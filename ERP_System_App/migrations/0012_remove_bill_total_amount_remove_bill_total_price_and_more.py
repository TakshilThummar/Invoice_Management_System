# Generated by Django 5.0.4 on 2024-08-15 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_System_App', '0011_bill_total_amount_bill_total_price_bill_total_tax'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='total_amount',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='total_price',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='total_tax',
        ),
    ]