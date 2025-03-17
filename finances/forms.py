from django import forms
from .models import Transaction, Budget, Investment, Goal, GoalContribution, Report, InvestmentSymbol

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
    symbol = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Enter symbol (e.g. AAPL)',
            'autocomplete': 'off'
        })
    )
    
    class Meta:
        model = Investment
        fields = ['symbol', 'name', 'shares', 'purchase_price', 'current_price']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Company or asset name'
            }),
            'shares': forms.NumberInput(attrs={
                'class': 'input',
                'step': '0.0001',
                'min': '0.0001',
                'placeholder': 'Number of shares or units'
            }),
            'purchase_price': forms.NumberInput(attrs={
                'class': 'input',
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'Price per share/unit'
            }),
            'current_price': forms.NumberInput(attrs={
                'class': 'input',
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'Current price per share/unit',
                'readonly': 'readonly'
            }),
        }
    
    def clean_symbol(self):
        symbol = self.cleaned_data['symbol'].upper()
        try:
            investment_symbol = InvestmentSymbol.objects.get(symbol=symbol)
        except InvestmentSymbol.DoesNotExist:
            raise forms.ValidationError(f"Symbol '{symbol}' does not exist.")
        return investment_symbol

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