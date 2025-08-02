from django.db import models


class ComponentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Component(models.Model):
    category = models.ForeignKey(
        ComponentCategory, on_delete=models.CASCADE, related_name="components"
    )
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    # Add more standardized fields as required
    specs = models.JSONField(
        default=dict, blank=True
    )  # Store arbitrary key-value pairs from the dataset

    def __str__(self):
        return f"{self.name} ({self.brand})"


class RetailerComponentOffer(models.Model):
    component = models.ForeignKey(
        "Component",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="offers",
    )
    retailer = models.CharField(max_length=30)
    retailer_name = models.CharField(max_length=255)
    model_name = models.CharField(max_length=128, blank=True, null=True)
    url = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    image_url = models.URLField(blank=True, null=True)
    availability = models.BooleanField(default=True)
    category = models.CharField(max_length=50)
