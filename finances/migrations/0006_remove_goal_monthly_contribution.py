# Generated by Django 4.2.7 on 2025-04-16 01:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0005_remove_investment_symbol_remove_investment_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='monthly_contribution',
        ),
    ]
