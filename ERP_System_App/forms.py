from django import forms
from .models import Bill, Customer
from django.contrib.auth.models import User
from .models import UserProfile

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['bill_number', 'customer_name', 'customer_number', 'address', 'bill_date', 'product_name', 'status', 'quantity', 'price', 'tax', 'total']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_id', 'customer_name', 'customer_number', 'customer_address', 'email', 'date_of_birth', 'age', 'gender']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'user_number', 'address', 'date_of_birth', 'age', 'gender', 'bio', 'profile_picture',]