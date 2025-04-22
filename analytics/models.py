# analytics/models.py
from django.db import models
from django.conf import settings

class Insight(models.Model):
    GOALS = 'goals'
    TRANSACTIONS_BUDGETS = 'transactions_budgets'

    INSIGHT_TYPE_CHOICES = [
        (GOALS, 'Goals'),
        (TRANSACTIONS_BUDGETS, 'Transactions & Budgets'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_insights'
    )
    prompt = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    insight_type = models.CharField(
        max_length=32,
        choices=INSIGHT_TYPE_CHOICES
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} – {self.get_insight_type_display()} @ {self.timestamp:%Y-%m-%d %H:%M}"