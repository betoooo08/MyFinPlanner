from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings


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
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    



class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField()
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
        # Validar que la contribución no exceda el monto restante de la meta
        if self.goal.current_amount + self.amount > self.goal.target_amount:
            raise ValidationError("La contribución excede el monto objetivo de la meta.")
        
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
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    
@receiver(pre_save, sender=Transaction)
def validate_and_update_budget(sender, instance, **kwargs):
    """
    Valida y actualiza el presupuesto asociado a una transacción de tipo 'expense'.
    Si no hay fondos suficientes en el presupuesto, lanza un ValidationError.
    """
    if instance.transaction_type == 'expense':
        try:
            # Buscar el presupuesto asociado a la categoría y usuario de la transacción
            budget = Budget.objects.get(user=instance.user, category=instance.category)
            new_spent = budget.spent + instance.amount

            # Verificar si el gasto excede el presupuesto
            if new_spent > budget.amount:
                raise ValidationError("No hay fondos suficientes en el presupuesto.")

            # Actualizar el campo 'spent' del presupuesto
            budget.spent = new_spent
            budget.save()
        except Budget.DoesNotExist:
            # Si no existe un presupuesto asociado, no se realiza ninguna acción
            pass