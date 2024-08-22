from django.db import models
from django.contrib.auth.models import User

class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    bill_number = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=100)
    customer_number = models.CharField(max_length=10, default='0000000000')
    address = models.CharField(max_length=1000, default='Default Address')
    bill_date = models.DateField()
    product_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('Pending', 'Pending'), ('Delay', 'Delay')], default='Cash')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bill #{self.bill_number} - {self.customer_name}"

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    customer_id = models.IntegerField(unique=True)
    customer_name = models.CharField(max_length=100)
    customer_number = models.CharField(max_length=10)
    customer_address = models.CharField(max_length=1000)
    email = models.EmailField()
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

    def __str__(self):
        return self.customer_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    user_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    bio = models.CharField(max_length=5000, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    #profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username