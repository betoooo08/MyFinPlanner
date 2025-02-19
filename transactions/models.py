from django.db import models

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