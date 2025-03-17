from django.apps import AppConfig
from django.db.models.signals import post_migrate

def seed_categories(sender, **kwargs):
    from .models import Category
    categories_data = [
        {"name": "Food", "category_type": "expense", "icon": "shopping-cart", "color": "#FF5733"},
        {"name": "Salary", "category_type": "income", "icon": "dollar-sign", "color": "#33FF57"},
        {"name": "Transport", "category_type": "expense", "icon": "truck", "color": "#3375FF"}
    ]
    for cat_data in categories_data:
        Category.objects.get_or_create(name=cat_data["name"], defaults=cat_data)

class FinancesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finances'

    def ready(self):
        post_migrate.connect(seed_categories, sender=self)