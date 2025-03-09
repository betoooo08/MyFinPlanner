from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ("Ingreso", "Ingreso"),
        ("Gasto", "Gasto"),
        ("Ahorro", "Ahorro"),
    ]

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.amount}"


class Budget(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('rent', 'Rent'),
        ('utilities', 'Utilities'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other'),
    ]
    allocated = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    remaining = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    def save(self, *args, **kwargs):
        self.allocated = self.allocated or Decimal('0.00')
        self.spent = self.spent or Decimal('0.00')
        self.remaining = self.allocated - self.spent  
        self.percentage = (self.spent / self.allocated) * Decimal(100) if self.allocated > Decimal('0.00') else Decimal('0.00')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.category}: {self.spent}/{self.allocated}"
