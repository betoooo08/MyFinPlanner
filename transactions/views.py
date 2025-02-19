from django.shortcuts import render, get_object_or_404, redirect
from .models import Transaction

def home(request):
    return render(request, "home.html")

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, "transaction_list.html", {"transactions": transactions})

def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, "transaction_detail.html", {"transaction": transaction})

def add_transaction(request):
    if request.method == "POST":
        title = request.POST["title"]
        amount = request.POST["amount"]
        category = request.POST["category"]
        description = request.POST["description"]
        date = request.POST["date"]
        
        Transaction.objects.create(
            title=title,
            amount=amount,
            category=category,
            description=description,
            date=date
        )
        return redirect("transaction_list")

    return render(request, "add_transaction.html")

def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.delete()
    return redirect("transaction_list")