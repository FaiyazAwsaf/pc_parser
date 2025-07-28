from django.db import models
from django.utils.text import slugify

class ComponentCategory(models.Model):
    """Model for component categories like CPU, GPU, Motherboard, etc."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Component Categories"

class Manufacturer(models.Model):
    """Model for component manufacturers like Intel, AMD, Nvidia, etc."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    logo = models.ImageField(upload_to='manufacturers/', blank=True, null=True)
    website = models.URLField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Component(models.Model):
    """Base model for all PC components"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    category = models.ForeignKey(ComponentCategory, on_delete=models.CASCADE, related_name='components')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='components')
    model_number = models.CharField(max_length=100, blank=True)
    release_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    specifications = models.JSONField(default=dict, blank=True)
    image = models.ImageField(upload_to='components/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.manufacturer.name}-{self.name}-{self.model_number}".strip('-'))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.manufacturer.name} {self.name}"
    
    class Meta:
        ordering = ['-created_at']

class ComponentPrice(models.Model):
    """Model to track component prices across different vendors"""
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='prices')
    vendor_name = models.CharField(max_length=255)
    vendor_url = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='BDT')  # Bangladesh Taka
    is_available = models.BooleanField(default=True)
    is_on_sale = models.BooleanField(default=False)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_checked = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.component.name} - {self.vendor_name} - {self.price} {self.currency}"
    
    class Meta:
        ordering = ['price']

class PriceHistory(models.Model):
    """Model to track historical price data for components"""
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='price_history')
    vendor_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='BDT')
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.component.name} - {self.price} {self.currency} - {self.recorded_at.date()}"
    
    class Meta:
        ordering = ['-recorded_at']
        verbose_name_plural = "Price Histories"