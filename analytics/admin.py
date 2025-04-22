# analytics/admin.py
from django.contrib import admin
from .models import Insight

@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ('user', 'insight_type', 'timestamp')
    list_filter = ('insight_type','timestamp')
    search_fields = ('user__username','prompt')