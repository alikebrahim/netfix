from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Q

from users.models import Company, Customer, User

from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


def create(request):
    # Check if user is authenticated and is a company
    if not request.user.is_authenticated or not request.user.is_company:
        return redirect('login_user')
    
    # Get company field
    company = Company.objects.get(user=request.user)
    company_field = company.field
    
    # Set choices based on company field
    choices = [(company_field, company_field)]
    
    if request.method == 'POST':
        form = CreateNewService(request.POST, choices=choices, company_field=company_field)
        if form.is_valid():
            # Create new service
            service = Service(
                company=company,
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price_hour=form.cleaned_data['price_hour'],
                field=form.cleaned_data['field']
            )
            service.save()
            return redirect('service_list')
    else:
        form = CreateNewService(choices=choices, company_field=company_field)
    
    return render(request, 'services/create.html', {'form': form})


def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


def request_service(request, id):
    # Check if user is authenticated and is a customer
    if not request.user.is_authenticated or not request.user.is_customer:
        return redirect('login_user')
    
    # Get service details
    service = Service.objects.get(id=id)
    customer = Customer.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            # Calculate total cost
            hours = form.cleaned_data['hours']
            total_cost = service.price_hour * hours
            
            # Create service request
            service_request = ServiceRequest(
                customer=customer,
                service=service,
                address=form.cleaned_data['address'],
                hours=hours,
                total_cost=total_cost
            )
            service_request.save()
            
            # Redirect to service list
            return redirect('services_list')
    else:
        form = RequestServiceForm()
    
    context = {
        'form': form,
        'service': service,
    }
    return render(request, 'services/request_service.html', context)


def search_services(request):
    query = request.GET.get('q', '')
    
    if query:
        results = Service.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(field__icontains=query) |
            Q(company__user__username__icontains=query)
        ).order_by('-date')
    else:
        results = Service.objects.all().order_by('-date')
    
    context = {
        'services': results,
        'query': query,
    }
    
    return render(request, 'services/search_results.html', context)
