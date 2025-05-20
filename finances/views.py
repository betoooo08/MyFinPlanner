from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import ValidationError
import finnhub
import datetime
import json
import requests
from decimal import Decimal
from .models import Transaction, Budget, Goal, Report, GoalContribution
from .forms import TransactionForm, BudgetForm, GoalForm, ReportForm
from investments.models import Investment, InvestmentSymbol
from investments.forms import InvestmentForm

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
    start_of_this_month = now.replace(day=1)
    end_of_last_month = start_of_this_month - datetime.timedelta(days=1)
    start_of_last_month = end_of_last_month.replace(day=1)

    this_month_income = transactions.filter(
        transaction_type='income', date__gte=start_of_this_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    last_month_income = transactions.filter(
        transaction_type='income', date__range=(start_of_last_month, end_of_last_month)
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    income_change_percentage = ((this_month_income - last_month_income) / last_month_income * 100) if last_month_income else 0

    this_month_expenses = transactions.filter(
        transaction_type='expense', date__gte=start_of_this_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    last_month_expenses = transactions.filter(
        transaction_type='expense', date__range=(start_of_last_month, end_of_last_month)
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    expenses_change_percentage = ((this_month_expenses - last_month_expenses) / last_month_expenses * 100) if last_month_expenses else 0

    this_month_balance = this_month_income - this_month_expenses
    last_month_balance = last_month_income - last_month_expenses
    balance_change_percentage = ((this_month_balance - last_month_balance) / last_month_balance * 100) if last_month_balance else 0

    savings_change_percentage = 0

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
    monthly_data = [{'name': m, 'income': monthly_dict[m]['income'], 'expenses': monthly_dict[m]['expenses']} for m in monthly_dict]

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
        'income_change_percentage': income_change_percentage,
        'expenses_change_percentage': expenses_change_percentage,
        'balance_change_percentage': balance_change_percentage,
        'savings_change_percentage': savings_change_percentage,
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

# ------------------------------------------------------------------
# Vistas de Transacciones
# ------------------------------------------------------------------
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
            try:
                transaction.save()  # Aquí se ejecutará la señal pre_save del modelo
                messages.success(request, "Transaction created successfully.")
                return redirect('transaction_list')
            except ValidationError as e:
                # Capturamos el error de validación y lo mostramos al usuario
                messages.error(request, e.message)
    else:
        form = TransactionForm()
    return render(request, 'transaction_form.html', {
        'form': form,
        'active_page': 'transaction_list'
    })

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'transaction_confirm_delete.html', {
        'transaction': transaction,
        'active_page': 'transaction_list'
    })

# ------------------------------------------------------------------
# Vistas de Budgets
# ------------------------------------------------------------------
@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)

    # Vinculamos transacciones a cada presupuesto
    for budget in budgets:
        budget.transactions = Transaction.objects.filter(
            user=request.user,
            category=budget.category
        )

    #  —————— ALERTAS DE PRESUPUESTO ——————
    for budget in budgets:
        pct = budget.percentage
        # Alcanza umbral (>= alert_threshold y <=100%)
        if pct >= budget.alert_threshold and pct <= 100:
            messages.warning(
                request,
                f'Has usado {pct}% de tu presupuesto "{budget.category.name}".'
            )
        # Lo supera (>100%)
        if pct > 100:
            messages.error(
                request,
                f'¡Has excedido tu presupuesto "{budget.category.name}" en {pct-100}%!'
            )

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
        'active_page': 'budget_list'
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
        'active_page': 'budget_list'
    })

@login_required
def delete_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        return redirect('budget_list')
    return render(request, 'budget_confirm_delete.html', {
        'budget': budget,
        'active_page': 'budget_list'
    })

# ------------------------------------------------------------------
# Vistas de Goals
# ------------------------------------------------------------------
@login_required
def goal_list(request):
    goals = Goal.objects.filter(user=request.user).order_by('deadline')
    return render(request, 'goals.html', {
        'goals': goals,
        'active_page': 'goals'
    })

@login_required
def ai_goal_insight(request):
    # 1) Siempre vuelvo a traer las metas
    goals = Goal.objects.filter(user=request.user).order_by('deadline')
    # 2) Aquí tu llamada a la IA, por ejemplo:
    # insight = run_your_ai_analysis(goals)
    insight = "Aquí iría tu análisis generado por IA…"  
    # 3) Renderizo de nuevo con goals + insight
    return render(request, 'goals.html', {
        'goals':       goals,
        'insight':     insight,
        'active_page': 'goals'
    })
    
@login_required
def create_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            # 1) Guardamos la meta sin aporte inicial
            goal = form.save(commit=False)
            goal.user = request.user
            goal.current_amount = Decimal('0')
            goal.save()

            # 2) Si vino aporte inicial, lo grabamos y actualizamos current_amount
            initial = form.cleaned_data.get('initial_contribution') or Decimal('0')
            if initial > 0:
                GoalContribution.objects.create(
                    goal=goal,
                    amount=initial,
                    date=timezone.now()
                )
                goal.current_amount = initial
                goal.save(update_fields=['current_amount'])

            messages.success(request, "Meta creada correctamente.")
            return redirect('goal_list')
    else:
        form = GoalForm()

    return render(request, 'goal_form.html', {
        'form': form,
        'active_page': 'goal_list'
    })

@login_required
def update_goal(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goal_list')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'goal_form.html', {
        'form': form,
        'active_page': 'goal_list'
    })

@login_required
def delete_goal(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        return redirect('goal_list')
    return render(request, 'goal_confirm_delete.html', {
        'goal': goal,
        'active_page': 'goal_list'
    })
    
@login_required
def add_contribution(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = Decimal(str(data.get('amount', 0)))
        if amount <= 0:
            return JsonResponse({'success': False, 'error': 'El monto debe ser mayor que 0.'})
        if (goal.current_amount + amount) > goal.target_amount:
            return JsonResponse({'success': False, 'error': 'La contribución excede el monto objetivo.'})

        # guardamos la nueva contribución
        GoalContribution.objects.create(goal=goal, amount=amount, date=timezone.now())

        # recalc current_amount desde contribuciones
        total = GoalContribution.objects.filter(goal=goal).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        goal.current_amount = total
        goal.save(update_fields=['current_amount'])

        pct = float(min(100, (total / goal.target_amount) * 100))
        remaining = float(goal.target_amount - total)
        return JsonResponse({
            'success':    True,
            'new_amount': float(total),
            'percentage': pct,
            'remaining':  remaining,
        })
    return JsonResponse({'success': False, 'error': 'Método no válido.'})

@login_required
def get_contributions(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    contributions = GoalContribution.objects.filter(goal=goal).order_by('-date')
    data = [
        {'amount': float(c.amount), 'date': c.date.strftime('%Y-%m-%d')}
        for c in contributions
    ]
    return JsonResponse({'success': True, 'contributions': data})
# ------------------------------------------------------------------
# Vistas de Reports
# ------------------------------------------------------------------
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
        'active_page': 'report_list'
    })

# ------------------------------------------------------------------
# Vistas de Investments
# ------------------------------------------------------------------
@login_required
def investment_list(request):
    investments = Investment.objects.filter(user=request.user)

    # Calcular métricas del portafolio
    total_portfolio_value = sum(inv.value for inv in investments)
    total_gain_value = sum((inv.current_price - inv.purchase_price) * inv.shares for inv in investments)
    total_purchase = sum(inv.purchase_price * inv.shares for inv in investments)
    total_gain_percent = (total_gain_value / total_purchase * 100) if total_purchase else Decimal('0')
    # Retorno diario (placeholder, podrías enriquecer)
    daily_return = Decimal('0')
    daily_return_percent = Decimal('0')
    total_portfolio_change = Decimal('0')  # Si tienes lógica histórica, sustitúyela aquí

    # Prepara JSON para gráficos
    investments_list = [{
        "symbol": inv.symbol.symbol,
        "symbol_type": inv.symbol.type,
        "name": inv.name,
        "shares": float(inv.shares),
        "purchase_price": float(inv.purchase_price),
        "current_price": float(inv.current_price),
        "value": float(inv.value),
    } for inv in investments]
    investments_json = json.dumps(investments_list)

    context = {
        'investments': investments,
        'stock_investments': investments.filter(symbol__type='Stock'),
        'crypto_investments': investments.filter(symbol__type='Crypto'),
        'total_portfolio_value': total_portfolio_value,
        'daily_return': daily_return,
        'daily_return_percent': daily_return_percent,
        'total_gain': total_gain_value,
        'total_gain_percent': total_gain_percent,
        'total_portfolio_change': total_portfolio_change,
        'investments_json': investments_json,
        'active_page': 'investments',   # <-- para que el link quede activo
    }
    return render(request, 'investments.html', context)


@login_required
def add_investment(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.user = request.user
            investment.symbol, _ = InvestmentSymbol.objects.get_or_create(
                symbol=form.cleaned_data['symbol']
            )
            investment.save()
            messages.success(request, "Investment added successfully.")
            return redirect('investment_list')
    else:
        form = InvestmentForm()
    return render(request, 'investment_form.html', {
        'form': form,
        'active_page': 'investments'
    })


@login_required
def delete_investment(request, pk):
    investment = get_object_or_404(Investment, pk=pk, user=request.user)
    if request.method == 'POST':
        investment.delete()
        messages.success(request, "Investment deleted.")
        return redirect('investment_list')
    return render(request, 'investment_confirm_delete.html', {
        'investment': investment,
        'active_page': 'investments'
    })


@login_required
def update_symbols(request):
    FINNHUB_API_KEY = settings.FINNHUB_API_KEY
    stock_url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={FINNHUB_API_KEY}"
    try:
        stock_response = requests.get(stock_url).json()
        bulk = []
        for stock in stock_response[:100]:
            if not InvestmentSymbol.objects.filter(symbol=stock['symbol']).exists():
                bulk.append(InvestmentSymbol(
                    symbol=stock['symbol'],
                    name=stock.get('description','Unknown'),
                    type='Stock'
                ))
        if bulk:
            InvestmentSymbol.objects.bulk_create(bulk)
            messages.success(request, f"Added {len(bulk)} new symbols.")
        else:
            messages.info(request, "No new symbols found.")
    except Exception as e:
        messages.error(request, f"Error updating symbols: {e}")
    return redirect('investment_list')


@login_required
def update_price(request):
    updated = 0
    for inv in Investment.objects.filter(user=request.user):
        new_price = get_stock_price(inv.symbol)
        if new_price > 0:
            inv.current_price = new_price
            inv.save()
            updated += 1
    messages.success(request, f"Updated prices for {updated} investments.")
    return redirect('investment_list')


def get_stock_price(symbol):
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={settings.FINNHUB_API_KEY}"
        resp = requests.get(url).json()
        return Decimal(str(resp.get("c", 0)))
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return Decimal('0')


@login_required
def symbol_search(request):
    q = request.GET.get('q','')
    results = []
    if q:
        try:
            data = finnhub_client.symbol_lookup(q).get('result',[])
            results = [{'symbol': it['symbol'], 'name': it['description']} for it in data]
        except Exception as e:
            print(f"Symbol search error: {e}")
    return JsonResponse(results, safe=False)


@login_required        # <-- añadimos login_required aquí también
def get_price(request, symbol):
    data = finnhub_client.quote(symbol)
    if 'c' in data:
        return JsonResponse({'price': data['c']})
    return JsonResponse({'error': 'Symbol not found'}, status=404)


