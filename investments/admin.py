from django.contrib import admin
from .models import Investment

# Register your models here.
@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'purchase_price', 'current_price', 'shares', 'value', 'change_percent')
    list_filter = ('symbol',)  # Filtra por campos válidos, como 'symbol'
    search_fields = ('symbol__symbol', 'name')  # Busca por el símbolo o el nombre
    readonly_fields = ('value', 'change', 'change_percent')  # Campos calculados como solo lectura
    fieldsets = (
        (None, {
            'fields': ('user', 'symbol', 'name', 'purchase_price', 'current_price', 'shares')
        }),
        ('Calculated Fields', {
            'fields': ('value', 'change', 'change_percent')
        }),
    )
