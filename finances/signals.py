from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, Budget
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Transaction)
def budget_limit_alert(sender, instance, created, **kwargs):
    # Solo en nuevas transacciones de tipo "expense"
    if not created or instance.transaction_type != 'expense':
        return

    try:
        budget = Budget.objects.get(user=instance.user, category=instance.category)
    except Budget.DoesNotExist:
        return

    # Si hemos llegado o pasado el umbral (%)
    if budget.percentage >= budget.alert_threshold:
        # Ejemplo: enviar un email (opcional)
        if instance.user.email:
            send_mail(
                subject=f"[MyFinPlanner] ¡Límite de presupuesto alcanzado!",
                message=(
                    f"Hola {instance.user.username},\n\n"
                    f"Has usado el {budget.percentage}% de tu presupuesto "
                    f"de «{budget.category.name}» (límite: {budget.amount})."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.user.email],
                fail_silently=True,
            )