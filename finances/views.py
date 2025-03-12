from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
import json

def dashboard(request):
    # Datos de ejemplo para tarjetas y gráficos
    total_balance = 12580.00
    total_income = 4550.00
    total_expenses = 2450.00
    total_savings = 2100.00
    monthly_data = [
        {'name': 'Jan', 'income': 4000, 'expenses': 2400},
        {'name': 'Feb', 'income': 3000, 'expenses': 1398},
        {'name': 'Mar', 'income': 2000, 'expenses': 3800},
        {'name': 'Apr', 'income': 2780, 'expenses': 3908},
        {'name': 'May', 'income': 1890, 'expenses': 4800},
        {'name': 'Jun', 'income': 2390, 'expenses': 3800},
        {'name': 'Jul', 'income': 3490, 'expenses': 4300},
    ]
    category_data = [
        {'name': 'Housing', 'value': 1200, 'color': '#0088FE'},
        {'name': 'Food', 'value': 600, 'color': '#00C49F'},
        {'name': 'Transportation', 'value': 300, 'color': '#FFBB28'},
        {'name': 'Entertainment', 'value': 200, 'color': '#FF8042'},
        {'name': 'Utilities', 'value': 150, 'color': '#8884d8'},
    ]
    budget_data = [
        {'name': 'Housing', 'budget': 1500, 'spent': 1200, 'percentage': 80},
        {'name': 'Food', 'budget': 800, 'spent': 600, 'percentage': 75},
        {'name': 'Transportation', 'budget': 400, 'spent': 300, 'percentage': 75},
        {'name': 'Entertainment', 'budget': 300, 'spent': 200, 'percentage': 67},
        {'name': 'Utilities', 'budget': 200, 'spent': 150, 'percentage': 75},
    ]
    recent_transactions = [
        {
            'type': 'expense',
            'description': 'Grocery Store',
            'date': timezone.now(),
            'amount': 85.25,
            'icon': 'arrow-down',
            'bg_class': 'bg-primary/10',
            'text_class': 'text-destructive'
        },
        {
            'type': 'income',
            'description': 'Salary Deposit',
            'date': timezone.now() - timedelta(days=1),
            'amount': 2250.00,
            'icon': 'arrow-up',
            'bg_class': 'bg-secondary/10',
            'text_class': 'text-secondary'
        },
        {
            'type': 'expense',
            'description': 'Electric Bill',
            'date': timezone.now() - timedelta(days=5),
            'amount': 94.50,
            'icon': 'arrow-down',
            'bg_class': 'bg-primary/10',
            'text_class': 'text-destructive'
        },
        {
            'type': 'expense',
            'description': 'Coffee Shop',
            'date': timezone.now() - timedelta(days=6),
            'amount': 4.75,
            'icon': 'arrow-down',
            'bg_class': 'bg-primary/10',
            'text_class': 'text-destructive'
        },
    ]
    ai_recommendations = [
        {
            'icon': 'lightbulb',
            'title': 'Spending Pattern',
            'description': 'Your restaurant spending is 30% higher than last month. Consider setting a dining budget.'
        },
        {
            'icon': 'lightbulb',
            'title': 'Savings Opportunity',
            'description': 'You could save $120/month by refinancing your current loan at today\'s rates.'
        },
        {
            'icon': 'bell',
            'title': 'Budget Alert',
            'description': 'Your entertainment budget is at 85% with 10 days left in the month.'
        },
    ]
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