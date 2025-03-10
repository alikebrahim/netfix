from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(
        validators=[validate_email],
        widget=forms.TextInput(attrs={'placeholder': 'Enter Email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Username'})
    )
    birth = forms.DateField(
        widget=DateInput(attrs={'placeholder': 'Date of Birth'})
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'birth']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"{username} is already taken.")
        return username

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(
            user=user,
            birth=self.cleaned_data.get('birth')
        )
        return user


class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(
        validators=[validate_email],
        widget=forms.TextInput(attrs={'placeholder': 'Enter Email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Username'})
    )
    field = forms.ChoiceField(
        choices=Company._meta.get_field('field').choices,
        widget=forms.Select(attrs={'placeholder': 'Select Field'})
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'field']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"{username} is already taken.")
        return username

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.save()
        company = Company.objects.create(
            user=user,
            field=self.cleaned_data.get('field')
        )
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
        
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password")
                
            user = authenticate(username=user.username, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password")
                
        return self.cleaned_data


class CustomerProfileEditForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Username'})
    )
    birth = forms.DateField(
        widget=DateInput(attrs={'placeholder': 'Date of Birth'})
    )

    class Meta:
        model = Customer
        fields = ['birth']

    def __init__(self, *args, **kwargs):
        super(CustomerProfileEditForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['email'].initial = self.instance.user.email
            self.fields['username'].initial = self.instance.user.username
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username', self.instance.user.username)
        
        # Check if email exists but exclude the current user
        if User.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError(f"{email} is already taken.")
        return email
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        current_username = self.instance.user.username
        
        # Check if username exists but exclude the current user
        if username != current_username and User.objects.filter(username=username).exists():
            raise ValidationError(f"{username} is already taken.")
        return username

    @transaction.atomic
    def save(self, commit=True):
        customer = super().save(commit=False)
        
        if commit:
            # Update User model fields
            user = customer.user
            user.email = self.cleaned_data.get('email')
            user.username = self.cleaned_data.get('username')
            user.save()
            
            customer.save()
            
        return customer


class CompanyProfileEditForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Username'})
    )
    field = forms.ChoiceField(
        choices=Company._meta.get_field('field').choices,
        widget=forms.Select(attrs={'placeholder': 'Select Field'})
    )

    class Meta:
        model = Company
        fields = ['field']

    def __init__(self, *args, **kwargs):
        super(CompanyProfileEditForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['email'].initial = self.instance.user.email
            self.fields['username'].initial = self.instance.user.username
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username', self.instance.user.username)
        
        # Check if email exists but exclude the current user
        if User.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError(f"{email} is already taken.")
        return email
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        current_username = self.instance.user.username
        
        # Check if username exists but exclude the current user
        if username != current_username and User.objects.filter(username=username).exists():
            raise ValidationError(f"{username} is already taken.")
        return username

    @transaction.atomic
    def save(self, commit=True):
        company = super().save(commit=False)
        
        if commit:
            # Update User model fields
            user = company.user
            user.email = self.cleaned_data.get('email')
            user.username = self.cleaned_data.get('username')
            user.save()
            
            company.save()
            
        return company
