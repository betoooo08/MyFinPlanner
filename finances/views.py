# finances/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.conf import settings
import datetime
import json
import requests
from .models import Transaction, Budget, Investment, InvestmentSymbol, Goal, Report
from .forms import TransactionForm, BudgetForm, InvestmentForm, GoalForm, ReportForm
import finnhub
from django.http import JsonResponse

# Configurar el cliente de Finnhub
finnhub_client = finnhub.Client(api_key=settings.FINNHUB_API_KEY)

@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    total_income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    total_balance = total_income - total_expenses
    total_savings = 0
    now = timezone.now()
    start_date = now - datetime.timedelta(days=180)
    monthly_tx = (
        transactions.filter(date__gte=start_date)
        .annotate(month=TruncMonth('date'))
        .values('month', 'transaction_type')
        .annotate(total=Sum('amount'))
        .order_by('month', 'transaction_type')
    )
    monthly_dict = {}
    for row in monthly_tx:
        m = row['month'].strftime('%b')
        if m not in monthly_dict:
            monthly_dict[m] = {'income': 0, 'expenses': 0}
        if row['transaction_type'] == 'income':
            monthly_dict[m]['income'] = float(row['total'])
        else:
            monthly_dict[m]['expenses'] = float(row['total'])
    monthly_data = []
    for m in monthly_dict:
        monthly_data.append({
            'name': m,
            'income': monthly_dict[m]['income'],
            'expenses': monthly_dict[m]['expenses']
        })
    last_30_days = now - datetime.timedelta(days=30)
    cat_tx = (
        transactions.filter(date__gte=last_30_days, transaction_type='expense')
        .values('category__name')
        .annotate(value=Sum('amount'))
    )
    color_palette = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#a29bfe', '#fd79a8']
    category_data = []
    idx = 0
    for row in cat_tx:
        category_data.append({
            'name': row['category__name'],
            'value': float(row['value']),
            'color': color_palette[idx % len(color_palette)]
        })
        idx += 1
    budgets = Budget.objects.filter(user=request.user)
    budget_data = []
    for b in budgets:
        budget_data.append({
            'name': b.category.name,
            'budget': float(b.amount),
            'spent': float(b.spent),
            'percentage': b.percentage
        })
    recent_transactions = transactions.order_by('-date')[:5]
    ai_recommendations = []
    context = {
        'total_balance': total_balance,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_savings': total_savings,
        'monthly_data': monthly_data,
        'monthly_data_json': json.dumps(monthly_data),
        'category_data': category_data,
        'category_data_json': json.dumps(category_data),
        'budget_data': budget_data,
        'recent_transactions': recent_transactions,
        'ai_recommendations': ai_recommendations,
        'active_page': 'dashboard',
    }
    return render(request, 'dashboard.html', context)

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'transactions.html', {
        'transactions': transactions,
        'active_page': 'transactions'
    })

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transaction_form.html', {
        'form': form,
        'active_page': 'transactions'
    })

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'transaction_confirm_delete.html', {
        'transaction': transaction,
        'active_page': 'transactions'
    })

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'budgets.html', {
        'budgets': budgets,
        'active_page': 'budgets'
    })

@login_required
def create_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'budget_form.html', {
        'form': form,
        'active_page': 'budgets'
    })

@login_required
def update_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'budget_form.html', {
        'form': form,
        'active_page': 'budgets'
    })

@login_required
def delete_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        return redirect('budget_list')
    return render(request, 'budget_confirm_delete.html', {
        'budget': budget,
        'active_page': 'budgets'
    })

@login_required
def investment_list(request):
    investments = Investment.objects.all()
    stock_investments = investments.filter(symbol__type='Stock')
    crypto_investments = investments.filter(symbol__type='Crypto')
    total_portfolio_value = sum(investment.value for investment in investments)

    context = {
        'investments': investments,
        'stock_investments': stock_investments,
        'crypto_investments': crypto_investments,
        'total_portfolio_value': total_portfolio_value,
    }
    return render(request, 'investments.html', context)

def add_investment(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            if request.user.is_authenticated:
                investment.user = request.user
            else:
                investment.user = None  # O maneja esto de otra manera según tus necesidades
            investment.save()
            return redirect('investment_list')
    else:
        form = InvestmentForm()
    return render(request, 'investment_form.html', {'form': form})

@login_required
def update_symbols(request):
    FINNHUB_API_KEY = settings.FINNHUB_API_KEY

    # Endpoint para obtener símbolos de acciones
    stock_url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={FINNHUB_API_KEY}"
    crypto_url = f"https://finnhub.io/api/v1/crypto/symbol?exchange=binance&token={FINNHUB_API_KEY}"

    try:
        stock_response = requests.get(stock_url).json()
        crypto_response = requests.get(crypto_url).json()

        # Guardar símbolos en la base de datos
        symbols_added = 0
        
        for stock in stock_response[:100]:  # Limitar a 100 para no sobrecargar
            obj, created = InvestmentSymbol.objects.get_or_create(
                symbol=stock['symbol'],
                defaults={'type': 'Stock'}
            )
            if created:
                symbols_added += 1

        for crypto in crypto_response[:50]:  # Limitar a 50 para no sobrecargar
            obj, created = InvestmentSymbol.objects.get_or_create(
                symbol=crypto['symbol'],
                defaults={'type': 'Crypto'}
            )
            if created:
                symbols_added += 1

        messages.success(request, f'Successfully updated symbols. Added {symbols_added} new symbols.')
    except Exception as e:
        messages.error(request, f'Error updating symbols: {str(e)}')

    return redirect('investment_list')


@login_required
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


@login_required
def symbol_search(request):
    query = request.GET.get('q', '')
    if query:
        data = finnhub_client.symbol_lookup(query)
        results = [{'symbol': item['symbol'], 'name': item['description']} for item in data.get('result', [])]
    else:
        results = []
    return JsonResponse(results, safe=False)

@login_required
def get_price(request, symbol):
    data = finnhub_client.quote(symbol)
    if 'c' in data:
        price = data['c']
        return JsonResponse({'price': price})
    else:
        return JsonResponse({'error': 'Symbol not found'}, status=404)

@login_required
def goal_list(request):
    goals = Goal.objects.filter(user=request.user)
    return render(request, 'goals.html', {
        'goals': goals,
        'active_page': 'goals'
    })

@login_required
def create_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goal_list')
    else:
        form = GoalForm()
    return render(request, 'goal_form.html', {
        'form': form,
        'active_page': 'goals'
    })

@login_required
def report_list(request):
    reports = Report.objects.filter(user=request.user)
    return render(request, 'reports.html', {
        'reports': reports,
        'active_page': 'reports'
    })

@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            return redirect('report_list')
    else:
        form = ReportForm()
    return render(request, 'report_form.html', {
        'form': form,
        'active_page': 'reports'
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})