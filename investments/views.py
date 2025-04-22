from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
import requests
from decimal import Decimal
from .models import Investment, InvestmentSymbol
from .forms import InvestmentForm
import finnhub
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
import random
import json

finnhub_client = finnhub.Client(api_key=settings.FINNHUB_API_KEY)

def investment_list(request):
    investments = Investment.objects.filter(user=request.user)  # Filtrar por usuario

    # Calcular el valor total del portafolio
    total_portfolio_value = sum(investment.value for investment in investments)

    # Calcular la ganancia/pérdida total
    total_gain = sum(investment.change for investment in investments)
    total_gain_percent = round((total_gain / total_portfolio_value) * 100, 2) if total_portfolio_value else 0

    # Calcular el retorno diario
    daily_return = sum((investment.current_price * Decimal(0.01)) * investment.shares for investment in investments)
    daily_return_percent = round((daily_return / total_portfolio_value) * 100, 2) if total_portfolio_value else 0

    # Calcular la distribución de activos para la gráfica de pastel
    asset_allocation = {}
    for investment in investments:
        if investment.name not in asset_allocation:
            asset_allocation[investment.name] = investment.value
        else:
            asset_allocation[investment.name] += investment.value

    # Convertir valores de asset_allocation a float
    asset_allocation = {key: float(value) for key, value in asset_allocation.items()}

    # Generar datos históricos simulados para la gráfica de crecimiento del portafolio
    portfolio_growth = generate_portfolio_history(total_portfolio_value)

    # Convertir valores de portfolio_growth a float
    portfolio_growth = [{'date': item['date'], 'value': float(item['value'])} for item in portfolio_growth]

    context = {
        'investments': investments,
        'total_portfolio_value': total_portfolio_value,
        'total_gain': total_gain,
        'total_gain_percent': total_gain_percent,
        'daily_return': daily_return,
        'daily_return_percent': daily_return_percent,
        'asset_allocation_json': json.dumps(asset_allocation),
        'portfolio_growth_json': json.dumps(portfolio_growth),
        'active_page': 'investments',
    }

    return render(request, 'investments.html', context)

def generate_portfolio_history(current_value):
    """
    Genera datos históricos simulados para el crecimiento del portafolio.
    En una implementación real, estos datos vendrían de una tabla de historial.
    """
    history = []
    today = datetime.now()
    
    # Generar datos para los últimos 12 meses
    for i in range(12):
        date = today - timedelta(days=30 * i)
        date_str = date.strftime('%Y-%m-%d')
        
        # Convertir valores a Decimal
        variation = Decimal(random.uniform(-0.05, 0.08))  # Variación entre -5% y 8%
        historic_value = current_value * (Decimal(1) - (Decimal(i) * Decimal(0.02)) + variation)
        
        history.append({
            'date': date_str,
            'value': round(historic_value, 2)  # Redondear a 2 decimales
        })
    
    # Ordenar por fecha (más antiguo primero)
    history.reverse()
    
    return history

def add_investment(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        print("Datos recibidos:", request.POST)
        
        if form.is_valid():
            print("Formulario válido")
            investment = form.save(commit=False)

            # Asignar el usuario autenticado
            investment.user = request.user

            # Verifica si el símbolo existe
            investment.symbol, _ = InvestmentSymbol.objects.get_or_create(symbol=form.cleaned_data['symbol'])
            print("Símbolo asignado:", investment.symbol)

            investment.save()
            print("Inversión guardada correctamente")
            return redirect('investment_list')

        else:
            print("Errores en el formulario:", form.errors)
    
    else:
        form = InvestmentForm()
    
    return render(request, 'investment_form.html', {'form': form})

def delete_investment(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    if request.method == 'POST':
        investment.delete()
        return redirect('investment_list')
    return render(request, 'investment_confirm_delete.html', {'investment': investment})
def update_symbols(request):
    FINNHUB_API_KEY = settings.FINNHUB_API_KEY
    stock_url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={FINNHUB_API_KEY}"

    try:
        stock_response = requests.get(stock_url).json()
        print(f"Received {len(stock_response)} stock symbols from API.")  # 🚨 DEBUG

        symbols_added = []
        bulk_create_list = []  # Lista para inserción masiva
        
        for stock in stock_response:
            if not InvestmentSymbol.objects.filter(symbol=stock['symbol']).exists():
                bulk_create_list.append(InvestmentSymbol(
                    symbol=stock['symbol'],
                    name=stock.get('description', 'Unknown'),
                    type='Stock'
                ))
                symbols_added.append(stock['symbol'])

        # Guardar en la base de datos con `bulk_create` (mucho más rápido)
        if bulk_create_list:
            InvestmentSymbol.objects.bulk_create(bulk_create_list)

        if symbols_added:
            messages.success(request, f'Successfully added {len(symbols_added)} new stocks: {", ".join(symbols_added[:50])}...')
        else:
            messages.info(request, "No new stocks were added.")

    except Exception as e:
        messages.error(request, f'Error updating symbols: {str(e)}')

    return redirect('investment_list')

def update_price(request):
    """Actualiza los precios de los investments añadidos por el usuario."""
    updated_count = 0

    # Filtrar solo los investments que el usuario ha agregado
    for investment in Investment.objects.all():
        symbol = investment.symbol
        new_price = get_stock_price(symbol)

        if new_price > 0:  # Evita actualizar con precios inválidos
            investment.current_price = new_price
            investment.save()
            updated_count += 1

    messages.success(request, f'Successfully updated prices for {updated_count} investments.')
    return redirect('investment_list')  # Ajusta esto según tu vista de inversiones


def get_stock_price(symbol):
    """Obtiene el precio actual de un símbolo desde Finnhub"""
    try:
        FINNHUB_API_KEY = settings.FINNHUB_API_KEY
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
        response = requests.get(url).json()
        return Decimal(str(response.get("c", 0)))  # "c" es el precio actual
    except Exception as e:
        print(f"Error al obtener precio para {symbol}: {e}")
        return Decimal('0')

def symbol_search(request):
    query = request.GET.get('q', '')
    if query:
        try:
            data = finnhub_client.symbol_lookup(query)
            print(f"Resultados de Finnhub para '{query}': {data}")  # 🚨 Depuración
            results = [{'symbol': item['symbol'], 'name': item['description']} for item in data.get('result', [])]
        except Exception as e:
            print(f"Error al buscar símbolos: {e}")  # 🚨 Depuración
            results = []
    else:
        results = []
    return JsonResponse(results, safe=False)


def get_price(request, symbol):
    data = finnhub_client.quote(symbol)
    if 'c' in data:
        price = data['c']
        return JsonResponse({'price': price})
    else:
        return JsonResponse({'error': 'Symbol not found'}, status=404)
