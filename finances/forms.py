from decimal import Decimal
from django import forms
from .models import Transaction, Budget, Goal, GoalContribution, Report

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'category', 'transaction_type', 'date', 'merchant']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'period', 'alert_threshold']

class GoalForm(forms.ModelForm):
    initial_contribution = forms.DecimalField(
        label="Initial Contribution",
        max_digits=12, decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'step':'0.01','min':'0'})
    )
    class Meta:
        model = Goal
        fields = ['name', 'target_amount', 'initial_contribution', 'deadline', 'description']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class GoalContributionForm(forms.ModelForm):
    class Meta:
        model = GoalContribution
        fields = ['amount', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'description', 'category', 'format', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }