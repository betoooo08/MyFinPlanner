from django import forms
from .models import Transaction
from .models import Budget

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['date']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'allocated']
        labels = {
            'category': 'Categoría',
            'allocated': 'Presupuesto Asignado',
        }
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Alimentación'}),
            'allocated': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 500'}),
        }
