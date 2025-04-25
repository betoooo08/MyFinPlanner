from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class InvestmentSymbol(models.Model):
    SYMBOL_TYPES = [
        ('Stock', 'Stock'),
        ('Crypto', 'Crypto'),
    ]
    
    symbol = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, default='unknown')
    type = models.CharField(max_length=10, choices=SYMBOL_TYPES)

    def __str__(self):
        return self.symbol

class Investment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    symbol = models.ForeignKey(InvestmentSymbol, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    shares = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=5, default=0.00)

    @property
    def value(self):
        return self.shares * self.current_price

    @property
    def change(self):
        return self.current_price - self.purchase_price

    @property
    def change_percent(self):
        if self.purchase_price == 0:
            return 0
        return (self.change / self.purchase_price) * 100

    def __str__(self):
        return f"{self.symbol.symbol}: {self.shares} shares"