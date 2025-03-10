from django import forms
from .models import Transaction, Budget

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'category', 'description', 'date']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'allocated']
        labels = {
            'category': 'Categoría',
            'allocated': 'Presupuesto Asignado',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'allocated': forms.NumberInput(attrs={'class': 'form-control'}),
        }