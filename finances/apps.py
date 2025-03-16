from django.apps import AppConfig

class FinancesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finances'

    def ready(self):
        from .models import Category
        default_categories = [
            {'name': 'Food', 'category_type': 'expense', 'icon': 'shopping-cart', 'color': '#FF5733'},
            {'name': 'Salary', 'category_type': 'income', 'icon': 'dollar-sign', 'color': '#00FF00'},
            {'name': 'Utilities', 'category_type': 'expense', 'icon': 'settings', 'color': '#0000FF'},
        ]
        for cat_data in default_categories:
            Category.objects.get_or_create(name=cat_data['name'], defaults=cat_data)