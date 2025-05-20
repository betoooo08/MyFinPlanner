# finances/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
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
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='monthly')
    alert_threshold = models.IntegerField(default=80)  # Porcentaje para alerta

    # Campos que evitan notificar dos veces
    notified_80 = models.BooleanField(default=False)
    notified_over = models.BooleanField(default=False)

    @property
    def remaining(self):
        return self.amount - self.spent

    @property
    def percentage(self):
        if self.amount == 0:
            return 0
        return int((self.spent / self.amount) * 100)

    def __str__(self):
        return f"{self.category.name} Budget: {self.spent}/{self.amount}"


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
        # Validar que no exceda la meta
        if self.goal.current_amount + self.amount > self.goal.target_amount:
            raise ValidationError("La contribución excede el monto objetivo de la meta.")
        super().save(*args, **kwargs)
        # Actualizar current_amount
        total = self.goal.contributions.aggregate(
            sum=models.Sum('amount')
        )['sum'] or 0
        self.goal.current_amount = total
        self.goal.save(update_fields=['current_amount'])

    def __str__(self):
        return f"Contribution to {self.goal.name}: {self.amount}"


class Report(models.Model):
    FORMAT_CHOICES = [
        ('pdf', 'PDF'), ('csv', 'CSV'),
        ('xlsx', 'Excel'), ('json', 'JSON'),
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


# ----------------------------------------------------
# Señal para actualizar Budget.spent antes de guardar Transaction
@receiver(pre_save, sender=Transaction)
def validate_and_update_budget(sender, instance, **kwargs):
    if instance.transaction_type == 'expense':
        try:
            budget = Budget.objects.get(user=instance.user, category=instance.category)
            new_spent = budget.spent + instance.amount
            if new_spent > budget.amount:
                raise ValidationError("No hay fondos suficientes en el presupuesto.")
            budget.spent = new_spent
            budget.save(update_fields=['spent'])
        except Budget.DoesNotExist:
            pass  # Sin presupuesto no hacemos nada

# Señal para enviar alertas cuando cruza threshold u 100 %
@receiver(post_save, sender=Transaction)
def budget_limit_alert(sender, instance, created, **kwargs):
    if not created or instance.transaction_type != 'expense':
        return

    try:
        budget = Budget.objects.get(user=instance.user, category=instance.category)
    except Budget.DoesNotExist:
        return

    pct = budget.percentage

    # Al llegar al alert_threshold (p.ej. 80%)
    if pct >= budget.alert_threshold and not budget.notified_80:
        send_mail(
            subject=f"⚠️ Tu presupuesto “{budget.category.name}” al {budget.alert_threshold} %",
            message=(
                f"Hola {budget.user.username},\n\n"
                f"Has usado {pct}% de tu presupuesto “{budget.category.name}” "
                f"(límite: ${budget.amount})."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[budget.user.email],
        )
        budget.notified_80 = True
        budget.save(update_fields=['notified_80'])

    # Al exceder el 100 %
    if pct > 100 and not budget.notified_over:
        send_mail(
            subject="❌ Has excedido tu presupuesto",
            message=(
                f"Hola {budget.user.username},\n\n"
                f"Has superado tu presupuesto “{budget.category.name}” en {pct - 100}%."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[budget.user.email],
        )
        budget.notified_over = True
        budget.save(update_fields=['notified_over'])