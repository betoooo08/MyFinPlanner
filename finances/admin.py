from django.contrib import admin
from .models import Category, Transaction, Budget, Investment, Goal, GoalContribution, Report

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'icon', 'color']
    list_filter = ['category_type']
    search_fields = ['name']
    fieldsets = (
        (None, {
            'fields': ('name', 'category_type', 'icon', 'color')
        }),
    )

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'description', 'category', 'transaction_type', 'date', 'merchant']
    list_filter = ['transaction_type', 'category', 'date']
    search_fields = ['description', 'merchant']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('user', 'amount', 'description', 'category', 'transaction_type', 'date', 'merchant')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at',),
        }),
    )

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'spent', 'remaining', 'percentage', 'period']
    list_filter = ['category', 'period']
    search_fields = ['user__username']
    readonly_fields = ['percentage', 'remaining']
    fieldsets = (
        (None, {
            'fields': ('user', 'category', 'amount', 'spent', 'period', 'alert_threshold')
        }),
        ('Calculated', {
            'classes': ('collapse',),
            'fields': ('percentage', 'remaining'),
        }),
    )

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'symbol', 'name', 'investment_type', 'purchase_price', 'current_price', 'shares', 'value']
    list_filter = ['investment_type', 'purchase_date']
    search_fields = ['symbol', 'name']
    readonly_fields = ['value', 'change', 'change_percent']
    fieldsets = (
        (None, {
            'fields': ('user', 'symbol', 'name', 'investment_type', 'shares', 'purchase_price', 'current_price', 'purchase_date')
        }),
        ('Calculated', {
            'classes': ('collapse',),
            'fields': ('value', 'change', 'change_percent'),
        }),
    )

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'target_amount', 'current_amount', 'percentage', 'deadline']
    list_filter = ['deadline']
    search_fields = ['name', 'description']
    readonly_fields = ['percentage', 'remaining']
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'target_amount', 'current_amount', 'deadline', 'monthly_contribution', 'description')
        }),
        ('Calculated', {
            'classes': ('collapse',),
            'fields': ('percentage', 'remaining'),
        }),
    )

@admin.register(GoalContribution)
class GoalContributionAdmin(admin.ModelAdmin):
    list_display = ['goal', 'amount', 'date']
    list_filter = ['date']
    search_fields = ['goal__name']
    fieldsets = (
        (None, {
            'fields': ('goal', 'amount', 'date')
        }),
    )

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'format', 'start_date', 'end_date', 'created_at']
    list_filter = ['category', 'format']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'description', 'category', 'format', 'start_date', 'end_date', 'file')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at',),
        }),
    )