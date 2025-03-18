from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('both', 'Both'),
    ]
    
    name = models.CharField(max_length=50, unique=True)
    category_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='expense')
    icon = models.CharField(max_length=50, blank=True, help_text="Nombre del icono (ej: 'home', 'shopping-cart')")
    color = models.CharField(max_length=20, blank=True, help_text="Código de color (ej: '#FF5733')")
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    # Cambiamos el campo category de CharField a ForeignKey
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date = models.DateField()
    merchant = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.transaction_type}: {self.amount} - {self.description}"

class Budget(models.Model):
    PERIOD_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Cambiamos el campo category de CharField a ForeignKey
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='monthly')
    alert_threshold = models.IntegerField(default=80)  # Porcentaje
    
    @property
    def remaining(self):
        return self.amount - self.spent
    
    @property
    def percentage(self):
        if self.amount == 0:
            return 0
        return int((self.spent / self.amount) * 100)
    
    def __str__(self):
        return f"{self.category.name} Budget: {self.amount}"
    

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    symbol = models.ForeignKey(InvestmentSymbol, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    shares = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

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

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField()
    monthly_contribution = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    
    @property
    def percentage(self):
        if self.target_amount == 0:
            return 0
        return int((self.current_amount / self.target_amount) * 100)
    
    @property
    def remaining(self):
        return self.target_amount - self.current_amount
    
    def __str__(self):
        return f"{self.name}: {self.current_amount}/{self.target_amount}"

class GoalContribution(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar el monto actual del objetivo
        self.goal.current_amount = sum(c.amount for c in self.goal.contributions.all())
        self.goal.save()
    
    def __str__(self):
        return f"Contribution to {self.goal.name}: {self.amount}"

class Report(models.Model):
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('csv', 'CSV'),
        ('xlsx', 'Excel'),
        ('json', 'JSON'),
    ]
    
    CATEGORY_CHOICES = [
        ('income-expense', 'Income & Expense'),
        ('budget', 'Budget Analysis'),
        ('investment', 'Investment Performance'),
        ('goals', 'Financial Goals'),
        ('net-worth', 'Net Worth'),
        ('tax', 'Tax Summary'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    file = models.FileField(upload_to='reports/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.format})"