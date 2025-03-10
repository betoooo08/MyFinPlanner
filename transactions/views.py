
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Budget
from .forms import BudgetForm, TransactionForm

def home(request):
    transactions = Transaction.objects.all().order_by('-date')[:5]  # Últimas 5 transacciones
    return render(request, 'dashboard.html', {'transactions': transactions})

def transactions_list(request):
    transactions = Transaction.objects.all()  # Obtiene todas las transacciones
    return render(request, "transaction_detail.html", {"transactions": transactions})

def create_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("transaction_list.html")
    else:
        form = TransactionForm()
    return render(request, "transaction_form.html", {"form": form})

def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'transaction_detail.html', {'transaction': transaction})

def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.delete()
    return redirect(request,'transaction_list.html')

def create_budget(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = BudgetForm()
    return render(request, "budget_form.html", {"form": form})
