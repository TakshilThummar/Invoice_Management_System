# Generated by Django 5.0.4 on 2024-08-18 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_System_App', '0021_alter_customer_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10),
        ),
    ]
