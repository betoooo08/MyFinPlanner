from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from decimal import Decimal
from .models import Transaction, Budget
from .forms import BudgetForm, TransactionForm

def home(request):
    # Suma de todas las transacciones con categoría "ingreso"
    total_ingresos = Transaction.objects.filter(category='ingreso') \
                                        .aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    # Suma de transacciones de tipo gasto
    total_gastos = Transaction.objects.filter(
        category__in=['food', 'rent', 'utilities', 'entertainment', 'other']
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # Balance = ingresos - gastos
    balance = total_ingresos - total_gastos

    # Últimas 5 transacciones para mostrar en el dashboard
    transactions = Transaction.objects.order_by('-date')[:5]

    return render(request, 'dashboard.html', {
        'transactions': transactions,
        'total_balance': balance,
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
    })

def transactions_list(request):
    transactions = Transaction.objects.all()
    return render(request, "transaction_list.html", {"transactions": transactions})

def create_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            # Si la transacción NO es "ingreso", actualizamos el presupuesto correspondiente
            if transaction.category in ['food', 'rent', 'utilities', 'entertainment', 'other']:
                try:
                    budget = Budget.objects.get(category=transaction.category)
                    budget.spent += transaction.amount
                    budget.save()  # actualiza remaining y percentage en el método save()
                except Budget.DoesNotExist:
                    pass
            return redirect("transaction_list")
    else:
        form = TransactionForm()
    return render(request, "transaction_form.html", {"form": form})

def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'transaction_detail.html', {'transaction': transaction})

def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    # (Opcional) Si deseas que al borrar se “devuelva” el monto al presupuesto, podrías restar:
    # if transaction.category in ['food', 'rent', 'utilities', 'entertainment', 'other']:
    #     try:
    #         budget = Budget.objects.get(category=transaction.category)
    #         budget.spent -= transaction.amount
    #         if budget.spent < 0:
    #             budget.spent = 0
    #         budget.save()
    #     except Budget.DoesNotExist:
    #         pass

    transaction.delete()
    return redirect("transaction_list")

def create_budget(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = BudgetForm()
    return render(request, "budget_form.html", {"form": form})