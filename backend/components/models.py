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
