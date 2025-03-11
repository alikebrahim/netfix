from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import Company, Customer


class Service(models.Model):
    """Model for services offered by companies."""
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=7)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], 
        default=0
    )
    choices = (
        ('Air Conditioner', 'Air Conditioner'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('House Keeping', 'House Keeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters'),
    )
    field = models.CharField(max_length=30, blank=False,
                         null=False, choices=choices)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    """Model for service requests from customers."""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    hours = models.DecimalField(
        decimal_places=2, 
        max_digits=5,
        validators=[MinValueValidator(0.5)]
    )
    request_date = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(decimal_places=2, max_digits=10)
    
    def __str__(self):
        return f"{self.customer} - {self.service} - {self.request_date}"
        
    class Meta:
        ordering = ['-request_date']
        verbose_name = "Service Request"
        verbose_name_plural = "Service Requests"
