# Generated by Django 5.1.5 on 2025-03-09 16:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_alter_transaction_category_alter_transaction_date_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('allocated', models.DecimalField(decimal_places=2, max_digits=10)),
                ('spent', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('remaining', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('percentage', models.DecimalField(decimal_places=2, editable=False, max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
