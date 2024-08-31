from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [


    path('', views.sign_in, name='sign_in'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('accounts/', include('allauth.urls')),


    path('home/', views.home, name='home'),
    path('monthly_totals/', views.monthly_totals, name='monthly_totals'),
    path('update_totals/', views.update_totals, name='update_totals'),
    path('get_totals/', views.get_totals, name='get_totals'),
    path('monthly_totals', views.monthly_totals, name='monthly_totals'),
    path('predict_next_30_days/', views.predict_next_30_days, name='predict_next_30_days'),


    path('bill_page', views.bill_page, name='bill_page'),
    path('edit_record', views.edit_record, name='edit_record'),


    path('generate_bill/', views.generate_bill, name='generate_bill'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),


    path('business', views.business, name='business'),


    path('generate_customer/', views.generate_customer, name='generate_customer'),
    path('delete_customers', views.delete_customers, name='delete_customers'),
    path('edit_customer', views.edit_customer, name='edit_customer'),  
      
    
    path('profile/', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),


    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)