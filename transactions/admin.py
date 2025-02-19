from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "category", "date")
    search_fields = ("title", "category")
    list_filter = ("category", "date")