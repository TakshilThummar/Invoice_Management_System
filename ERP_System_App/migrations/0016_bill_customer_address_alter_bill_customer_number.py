# Generated by Django 5.0.4 on 2024-08-17 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_System_App', '0015_bill_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='customer_address',
            field=models.CharField(default='Default Value', max_length=500),
        ),
        migrations.AlterField(
            model_name='bill',
            name='customer_number',
            field=models.CharField(default='0000000000', max_length=10),
        ),
    ]
