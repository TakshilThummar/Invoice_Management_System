import csv
from datetime import datetime, timezone
import json
import os
from statistics import LinearRegression
import pandas as pd
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Bill, Customer
from .forms import BillForm, CustomerForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.utils import timezone
from sklearn.linear_model import LinearRegression
from datetime import datetime
from .forms import UserForm, UserProfileForm
from .models import UserProfile

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Sign In Successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('sign_in')
        
    return render(request, 'sign_in.html')

def sign_up(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('sign_up')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('sign_up')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('sign_up')
        
        User.objects.create_user(username=username, email=email, password=password)

        messages.success(request, "Sign Up Successful! Please sign in.")

        return redirect('sign_in')
    
    return render(request, 'sign_up.html')

def sign_out(request):
    logout(request)
    messages.info(request, "You Have Been Logged Out.")
    return redirect('sign_in')

@login_required
def home(request):
    user = request.user
    
    # Filter bills and customers by the logged-in user
    bills = Bill.objects.filter(user=user)
    customers = Customer.objects.filter(user=user)
    
    # Count bills specific to the user
    bill_count = bills.count()

    # Count unique customers associated with the user's bills
    unique_customers = bills.values('customer_name').distinct().count()

    # Filter and count bills based on their status for the logged-in user
    cash_bills = bills.filter(status='Cash').count()
    delay_bills = bills.filter(status='Delay').count()
    pending_bills = bills.filter(status='Pending').count()

    context = {
        'bills': bills,
        'customers': customers,
        'bill_count': bill_count,
        'unique_customers': unique_customers,
        'cash_bills': cash_bills,
        'delay_bills': delay_bills,
        'pending_bills': pending_bills,
    }

    return render(request, 'home.html', context)


@login_required
def generate_bill(request):
    if request.method == "POST":
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user
            bill.save()
            messages.success(request, "Bill generated successfully.")
            return redirect('bill_page')
    else:
        form = BillForm()

    last_bill = Bill.objects.order_by('id').last()
    next_bill_number = last_bill.id + 1 if last_bill else 1

    context = {'form': form, 'next_bill_number' : next_bill_number}

    return render(request, 'generate_bill.html', context)

@login_required
def generate_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            messages.success(request, "Customer added successfully.")
            return redirect('business')
    else:
        form = CustomerForm()

    last_customer = Customer.objects.last()
    next_id = (last_customer.id + 1) if last_customer else 1

    context = {'form': form, 'next_id' : next_id}

    return render(request, 'generate_customer.html', context)

def generate_pdf(request):
    bill_number = request.GET.get('bill_number', '')
    bill = get_object_or_404(Bill, bill_number=bill_number, user=request.user)
    data = {
        'bill_number': bill.bill_number,
        'customer_name': bill.customer_name,
        'customer_number': bill.customer_number,
        'date': bill.bill_date,
        'product_name': bill.product_name,
        'quantity': bill.quantity,
        'price': bill.price,
        'tax': bill.tax,
        'total': bill.total,
    }
    html_string = render_to_string('pdf_template.html', data)
    pdf_file = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{bill_number}.pdf"'
    return response

def monthly_totals(request):
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    # Initialize an empty list to store the totals
    total_date_amount = []

    for day in range(1, 32):  # Assuming max 31 days in a month
        try:
            # Create a date object for the day
            date = timezone.datetime(current_year, current_month, day)
        except ValueError:
            break  # Handle cases where the day is out of range for the month

        # Calculate daily total for the specific day
        daily_total = Bill.objects.filter(bill_date__year=current_year, bill_date__month=current_month, bill_date__day=day).aggregate(total=Sum('total'))['total']
        
        # Append the result to the list
        total_date_amount.append({
            'date': date.strftime('%Y-%m-%d'),
            'total': daily_total if daily_total else 0
        })  

    # File path for the CSV
    file_path = os.path.expanduser('~/Downloads/revenue.csv')
    
    # Write data to CSV
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Total'])
        for row in total_date_amount:
            writer.writerow([row['date'], row['total']])
    
    # Return the JSON data
    return JsonResponse(total_date_amount, safe=False)

def bill_page(request):
    bills = Bill.objects.all()
    if request.method == "POST":
        ids_to_delete = request.POST.getlist('delete')
        Bill.objects.filter(id__in=ids_to_delete).delete()
        return redirect('bill_page')
    
    user = request.user
    bills = Bill.objects.filter(user=user)
    customers = Customer.objects.filter(user=user)

    context = {
        'bills': bills,
        'customers': customers,
    }
    return render(request, 'bill_page.html', context)


def business(request):
    user = request.user
    bills = Bill.objects.filter(user=user)
    customers = Customer.objects.filter(user=user) # Fetch login customer from the database

    context = {
        'bills': bills,
        'customers': customers,
    }

    return render(request, 'business.html', context)


@require_POST
def edit_record(request):
    record_id = request.POST.get('id')
    bill_number = request.POST.get('bill_number')
    customer_name = request.POST.get('customer_name')
    customer_number = request.POST.get('customer_number')
    address = request.POST.get('address')
    date = request.POST.get('date')
    product_name = request.POST.get('product_name')
    status = request.POST.get('status')
    quantity = request.POST.get('quantity')
    price = request.POST.get('price')
    tax = request.POST.get('tax')
    total = request.POST.get('total')  

    # Fetch the record and update it
    bill = Bill.objects.get(id=record_id)
    bill.bill_number = bill_number
    bill.customer_name = customer_name
    bill.customer_number = customer_number
    bill.address = address
    bill.bill_date = date
    bill.product_name = product_name
    bill.status = status
    bill.quantity = quantity
    bill.price = price
    bill.tax = tax
    bill.total = total
    bill.save()

    print(price, tax, total, quantity, status, product_name, customer_name, customer_number, address, bill_number)

    return redirect('bill_page')

def delete_customers(request):
    if request.method == "POST":
        customer_ids = request.POST.getlist('customer_delete')
        Customer.objects.filter(id__in=customer_ids).delete()
        messages.success(request, "Record(s) Deleted Successfully...")
        return redirect('business')
    return redirect('business')

def edit_customer(request):
    if request.method == 'POST':
        # Retrieve and update the record
        customer_id = request.POST.get('id')
        customer_name = request.POST.get('customer_name')
        customer_number = request.POST.get('customer_number')
        customer_address = request.POST.get('customer_address')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        age = request.POST.get('age')

        print(customer_id, customer_name, customer_number, customer_address, email, date_of_birth, gender, age)

        # Get the customer object
        customer = get_object_or_404(Customer, id=customer_id)

        # Update the customer fields
        customer.customer_id = customer_id
        customer.customer_name = customer_name
        customer.customer_number = customer_number
        customer.customer_address = customer_address
        customer.email = email
        customer.date_of_birth = date_of_birth
        customer.gender = gender
        customer.age = age

        # Save the updated customer record
        customer.save()

        messages.success(request, 'Record updated successfully.')

        return redirect('business')  # Replace with your redirect URL or name

    return redirect('business')  # Handle cases where method is not POST

def update_totals(request):

    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))
        total_amount = float(data.get('total_amount'))
        total_tax = float(data.get('total_tax'))
        total_price = float(data.get('total_price'))     

        # save the totals to the database or session

        # for this example, we'll just store them in a dictionary

        request.session['totals'] = {'total_amount': total_amount, 'total_tax': total_tax, 'total_price': total_price}

        #print(f"Updated totals: {totals}")

        return JsonResponse({'message': 'Totals updated successfully'})

    return HttpResponse('Invalid request')

def get_totals(request):
    user = request.user

    # Retrieve the totals from the session or use defaults
    totals = request.session.get('totals', {'total_amount': 0, 'total_tax': 0, 'total_price': 0})

    # Filter by user and calculate totals by month
    totals_by_month = Bill.objects.filter(user=user).values('bill_date__month').annotate(total_amount=Sum('total')).order_by('bill_date__month')

    monthly_totals = {
        datetime(1900, item['bill_date__month'], 1).strftime('%b'): float(item['total_amount'])
        for item in totals_by_month
    }

    # Create a list of all months for reference
    months = [datetime(1900, i, 1).strftime('%b') for i in range(1, 13)]
    monthly_amounts = [monthly_totals.get(month, 0) for month in months]

    # Get the status counts, filtered by the logged-in user
    status_counts = Bill.objects.filter(user=user).values('status').annotate(count=Count('id'))
    data = {status['status']: status['count'] for status in status_counts}

    response_data = {
        'totals': totals,
        'months': months,
        'monthly_totals': monthly_amounts,
        'data': data
    }

    return JsonResponse(response_data)

def monthly_totals(request):
    user = request.user
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    # Initialize an empty list to store the totals
    total_date_amount = []

    for day in range(1, 32):  # Assuming max 31 days in a month
        try:
            # Create a date object for the day
            date = datetime(current_year, current_month, day)
        except ValueError:
            break  # Handle cases where the day is out of range for the month

        # Calculate daily total for the specific day, filtered by the logged-in user
        daily_total = Bill.objects.filter(
            user=user,
            bill_date__year=current_year,
            bill_date__month=current_month,
            bill_date__day=day
        ).aggregate(total=Sum('total'))['total']
        
        # Append the result to the list
        total_date_amount.append({
            'date': date.strftime('%Y-%m-%d'),
            'total': daily_total if daily_total else 0
        })

    # File path for the CSV
    file_path = os.path.expanduser('~/Downloads/revenue.csv')
    
    # Write data to CSV
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Total'])
        for row in total_date_amount:
            writer.writerow([row['date'], row['total']])
    
    # Return the JSON data
    return JsonResponse(total_date_amount, safe=False)

def predict_next_30_days(request):
    today = timezone.now()
    
    # Retrieve data for the past 30 days
    start_date = today - timezone.timedelta(days=30)
    data = list(Bill.objects.filter(user=request.user, bill_date__gte=start_date).values('bill_date', 'total'))

    if not data:
        return JsonResponse({'error': 'Not enough data for prediction.'}, status=400)
    
    # Prepare data for training
    df = pd.DataFrame(data)
    df['bill_date'] = pd.to_datetime(df['bill_date'])
    df.set_index('bill_date', inplace=True)
    df = df.resample('D').sum().fillna(0)  # Resample to daily frequency
    
    # Create features and labels
    df['day'] = np.arange(len(df))
    X = df[['day']].values
    y = df['total'].values
    
    # Train the model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict the next 30 days
    future_days = np.arange(len(df), len(df) + 30).reshape(-1, 1)
    predictions = model.predict(future_days)
    
    # Prepare the response
    future_dates = [(today + timezone.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 31)]
    predicted_revenue = [{'date': date, 'predicted_total': round(pred, 2)} for date, pred in zip(future_dates, predictions)]

    # Prepare data for radar chart
    radar_data = {
        'labels': future_dates,
        'datasets': [{
            'label': 'Predicted Revenue',
            'data': predictions.tolist(),
            'backgroundColor': 'rgba(255, 99, 132, 0.2)',
            'borderColor': 'rgba(255, 99, 132, 1)',
            'borderWidth': 1
        }]
    }
    
    return JsonResponse(radar_data, safe=False)

@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')    

    else:
        form = UserProfileForm(instance=user_profile)

    formatted_date_of_birth = user_profile.date_of_birth.strftime('%Y-%m-%d') if user_profile.date_of_birth else ''

    context = {
        'form': form,
        'formatted_date_of_birth': formatted_date_of_birth,
    }
    
    return render(request, 'edit_profile.html', context)

'''@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    formatted_date_of_birth = user_profile.date_of_birth.strftime('%Y-%m-%d') if user_profile.date_of_birth else ''

    context = {
        'user_profile': user_profile,
        'formatted_date_of_birth': formatted_date_of_birth,
        'profile_picture': user_profile.profile_picture.url if user_profile.profile_picture else None,
    }

    return render(request, 'profile.html', context)'''

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if user_profile.date_of_birth:
        formatted_date_of_birth = user_profile.date_of_birth.strftime('%Y-%m-%d')
    else:
        formatted_date_of_birth = ''
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'user_profile': user_profile,
        'formatted_date_of_birth': formatted_date_of_birth,
        'profile_picture': user_profile.profile_picture.url if user_profile.profile_picture else None,
        'form': form,
    }
    
    return render(request, 'profile.html', context)
