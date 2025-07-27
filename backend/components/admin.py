from django.contrib import admin
from .models import ComponentCategory, Manufacturer, Component, ComponentPrice, PriceHistory

@admin.register(ComponentCategory)
class ComponentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'category', 'model_number', 'is_active')
    list_filter = ('category', 'manufacturer', 'is_active')
    search_fields = ('name', 'model_number', 'manufacturer__name')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ComponentPrice)
class ComponentPriceAdmin(admin.ModelAdmin):
    list_display = ('component', 'vendor_name', 'price', 'currency', 'is_available', 'last_checked')
    list_filter = ('vendor_name', 'is_available', 'is_on_sale')
    search_fields = ('component__name', 'vendor_name')
    readonly_fields = ('last_checked', 'created_at')

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('component', 'vendor_name', 'price', 'currency', 'recorded_at')
    list_filter = ('vendor_name', 'recorded_at')
    search_fields = ('component__name', 'vendor_name')
    readonly_fields = ('recorded_at',)