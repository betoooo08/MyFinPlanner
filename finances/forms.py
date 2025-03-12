from django import forms
from .models import Transaction, Budget, Investment, Goal, GoalContribution, Report

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

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['symbol', 'name', 'investment_type', 'shares', 'purchase_price', 'current_price', 'purchase_date']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'target_amount', 'current_amount', 'deadline', 'monthly_contribution', 'description']
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