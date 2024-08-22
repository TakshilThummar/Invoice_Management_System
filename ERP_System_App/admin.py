from django.contrib import admin
from .models import Bill
from .models import Customer
from .models import UserProfile

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_number', 'customer_name', 'customer_number', 'address', 'bill_date', 'product_name', 'quantity', 'price', 'tax', 'total', 'status')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'customer_name', 'customer_number', 'customer_address', 'email', 'age', 'date_of_birth', 'gender')

admin.site.register(UserProfile)