from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from datetime import date

from users.models import User, Company, Customer
from users.forms import CustomerProfileEditForm, CompanyProfileEditForm
from services.models import Service, ServiceRequest


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request, name):
    # Get the customer user and their service requests
    user = User.objects.get(username=name)
    customer = Customer.objects.get(user=user)
    
    # Calculate user age from birth date
    today = date.today()
    birth_date = customer.birth
    user_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    # Get service history (all service requests)
    service_history = ServiceRequest.objects.filter(customer=customer).order_by("-request_date")
    
    return render(request, 'users/profile.html', {
        'user': user, 
        'user_age': user_age, 
        'sh': service_history
    })


def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    services = Service.objects.filter(
        company=Company.objects.get(user=user)).order_by("-date")

    return render(request, 'users/profile.html', {'user': user, 'services': services})


@login_required
def edit_customer_profile(request, name):
    # Ensure the logged-in user is accessing their own profile
    if request.user.username != name or not request.user.is_customer:
        return HttpResponseForbidden("You don't have permission to edit this profile")
    
    customer = Customer.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = CustomerProfileEditForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_profile', name=form.cleaned_data.get('username'))
    else:
        form = CustomerProfileEditForm(instance=customer)
    
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def edit_company_profile(request, name):
    # Ensure the logged-in user is accessing their own profile
    if request.user.username != name or not request.user.is_company:
        return HttpResponseForbidden("You don't have permission to edit this profile")
    
    company = Company.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = CompanyProfileEditForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_profile', name=form.cleaned_data.get('username'))
    else:
        form = CompanyProfileEditForm(instance=company)
    
    return render(request, 'users/edit_profile.html', {'form': form})
