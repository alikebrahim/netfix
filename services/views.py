from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from users.models import Company, Customer
from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm

# Reference field choices from the Service model


def service_list(request):
    """Show list of all services."""
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    """Show details for a single service."""
    service = get_object_or_404(Service, id=id)
    return render(request, 'services/single_service.html', {'service': service})


@login_required
def create(request):
    """Create a new service."""
    # Check if user is a company
    if not request.user.is_company:
        return redirect('login_user')
    
    # Get company field
    company = Company.objects.get(user=request.user)
    company_field = company.field
    
    # Set choices based on company field
    if company_field == 'All in One':
        choices = Service.choices
        company_field = None  # Allow all fields for 'All in One' companies
    else:
        choices = [(company_field, company_field)]
    
    if request.method == 'POST':
        form = CreateNewService(request.POST, choices=choices, company_field=company_field)
        
        # Check if the company is trying to create a service in a field they're not allowed to
        if form.is_valid():
            field = form.cleaned_data['field']
            
            # Additional validation - double check that the company can create this type of service
            if company_field is not None and field != company_field:
                form.add_error('field', f"Your company is registered as a '{company_field}' provider. You can only create services in this field.")
            else:
                # Create new service
                service = Service(
                    company=company,
                    name=form.cleaned_data['name'],
                    description=form.cleaned_data['description'],
                    price_hour=form.cleaned_data['price_hour'],
                    field=form.cleaned_data['field']
                )
                service.save()
                return redirect('services_list')
    else:
        form = CreateNewService(choices=choices, company_field=company_field)
    
    context = {
        'form': form,
        'company_field': company_field,
        'is_all_in_one': company_field == 'All in One'
    }
    
    return render(request, 'services/create.html', context)


def service_field(request, field):
    """Show services filtered by field."""
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


@login_required
def request_service(request, id):
    """Request a service."""
    # Check if user is a customer
    if not request.user.is_customer:
        return redirect('login_user')
    
    # Get service details
    service = get_object_or_404(Service, id=id)
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

