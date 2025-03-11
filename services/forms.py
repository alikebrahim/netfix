from django import forms
from .models import Service


class CreateNewService(forms.Form):
    """Form for creating a new service."""
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(
        decimal_places=2, max_digits=5, min_value=0.00)
    field = forms.ChoiceField(required=True)
    company_field = None  # Store the company's field for validation

    def __init__(self, *args, choices=None, company_field=None, **kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        self.company_field = company_field
        
        # adding choices to fields
        if choices:
            self.fields['field'].choices = choices
        else:
            self.fields['field'].choices = Service.choices
        
        # adding placeholders to form fields
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'
        self.fields['price_hour'].widget.attrs['step'] = '0.1'  # Set step to 0.1
        self.fields['name'].widget.attrs['autocomplete'] = 'off'
    
    def clean_field(self):
        field = self.cleaned_data.get('field')
        if self.company_field and field != self.company_field:
            raise forms.ValidationError(f"You can only create services in your field: {self.company_field}")
        return field


class RequestServiceForm(forms.Form):
    """Form for requesting a service."""
    address = forms.CharField(max_length=255)
    hours = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        min_value=0.5,
        label='Number of hours needed'
    )
    
    def __init__(self, *args, **kwargs):
        super(RequestServiceForm, self).__init__(*args, **kwargs)
        # Adding placeholders
        self.fields['address'].widget.attrs['placeholder'] = 'Enter your address'
        self.fields['hours'].widget.attrs['placeholder'] = 'Enter hours needed (minimum 0.5)'
        self.fields['hours'].widget.attrs['step'] = '0.1'  # Set step to 0.1
