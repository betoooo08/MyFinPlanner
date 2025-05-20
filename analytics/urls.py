from django.urls import path
from . import views

urlpatterns = [
    path(
        'ai-goal-insight/',
        views.AI_Goal_Insight,
        name='ai_goal_insight'
    ),
    path(
        'ai-transactions-budgets-insight/',
        views.AI_Transactions_and_Budgets_Insight,
        name='ai_transactions_and_budgets_insight'
    ),
    # En tu archivo urls.py
path('reports/export/pdf/', views.export_financial_report_pdf, name='export_financial_report_pdf'),
path('reports/export/csv/', views.export_financial_report_csv, name='export_financial_report_csv'),
]