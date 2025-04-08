from django.urls import path
from django.contrib.auth import views as auth_views

from .forms import UserLoginForm
from . import views as v

# Main user URLs
urlpatterns = [
    # Registration URL patterns
    path('', v.register, name='register'),
    path('register/', v.register, name='register'),
    
    # Company registration
    path('company/', v.CompanySignUpView.as_view(), name='register_company'),
    path('register/company/', v.CompanySignUpView.as_view(), name='register_company'),
    
    # Customer registration
    path('customer/', v.CustomerSignUpView.as_view(), name='register_customer'),
    path('register/customer/', v.CustomerSignUpView.as_view(), name='register_customer'),
    
    # Login URL
    path('login/', v.LoginUserView, name='login_user'),
]
