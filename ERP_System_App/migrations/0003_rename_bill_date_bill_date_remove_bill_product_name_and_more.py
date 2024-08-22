# Generated by Django 5.0.4 on 2024-08-12 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_System_App', '0002_rename_date_bill_bill_date_rename_amount_bill_price_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bill',
            old_name='bill_date',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='product_name',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='total_amount',
        ),
        migrations.AddField(
            model_name='bill',
            name='product',
            field=models.CharField(default='default_product', max_length=255),
        ),
        migrations.AddField(
            model_name='bill',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='bill',
            name='customer_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bill',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]