from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('CPU', 'CPU'),
        ('RAM', 'RAM'),
        ('Storage', 'Storage'),
        ('Monitor', 'Monitor'),
        ('Motherboard', 'Motherboard'),
        ('PSU', 'PSU'),
    ]
    
    CONDITION_CHOICES = [
        ('Used-Like New', 'Used-Like New'),
        ('Used-Good', 'Used-Good'),
        ('Used-Fair', 'Used-Fair'),
    ]
    
    AGE_CHOICES = [
        ('0-6months', 'Less than 6 months'),
        ('6-12months', '6-12 months'),
        ('1-2years', '1-2 years'),
        ('2plus', '2+ years'),
    ]
    
    WARRANTY_CHOICES = [
        ('under', 'Under warranty'),
        ('expired', 'Warranty expired'),
        ('none', 'No warranty info'),
    ]
    
    BOX_ACCESSORIES_CHOICES = [
        ('box', 'Has original box'),
        ('accessories', 'Has all accessories'),
        ('missing', 'Missing items'),
    ]
    
    PRICE_TYPE_CHOICES = [
        ('fixed', 'Fixed price'),
        ('negotiable', 'Price negotiable'),
    ]
    
    AVAILABILITY_CHOICES = [
        ('now', 'Available now'),
        ('soon', 'Available soon'),
    ]
    
    BRAND_CHOICES = [
        ('intel', 'Intel'),
        ('amd', 'AMD'),
        ('nvidia', 'NVIDIA'),
        ('asus', 'ASUS'),
        ('msi', 'MSI'),
        ('corsair', 'Corsair'),
        ('gigabyte', 'Gigabyte'),
        ('evga', 'EVGA'),
        ('samsung', 'Samsung'),
        ('western-digital', 'Western Digital'),
    ]
    
    COMPATIBILITY_CHOICES = [
        ('lga1700', 'LGA1700'),
        ('am4', 'AM4'),
        ('am5', 'AM5'),
        ('ddr4', 'DDR4'),
        ('ddr5', 'DDR5'),
        ('atx', 'ATX'),
        ('micro-atx', 'Micro-ATX'),
        ('mini-itx', 'Mini-ITX'),
    ]
    
    PERFORMANCE_TIER_CHOICES = [
        ('entry', 'Entry level'),
        ('mid', 'Mid-range'),
        ('high', 'High-end'),
    ]
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    # New filter fields - null=True for migration, blank=False for forms
    age = models.CharField(max_length=20, choices=AGE_CHOICES, null=True, blank=False)
    warranty = models.CharField(max_length=20, choices=WARRANTY_CHOICES, null=True, blank=False)
    box_accessories = models.CharField(max_length=20, choices=BOX_ACCESSORIES_CHOICES, null=True, blank=False)
    price_type = models.CharField(max_length=20, choices=PRICE_TYPE_CHOICES, default='fixed')
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='now')
    brand = models.CharField(max_length=30, choices=BRAND_CHOICES, null=True, blank=False)
    compatibility = models.CharField(max_length=20, choices=COMPATIBILITY_CHOICES, blank=True)
    performance_tier = models.CharField(max_length=20, choices=PERFORMANCE_TIER_CHOICES, null=True, blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.seller.username}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"

class Chat(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='chats')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_chats')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['product', 'buyer', 'seller']
    
    def __str__(self):
        return f"Chat for {self.product.name} - {self.buyer.username} & {self.seller.username}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message from {self.sender.username} in {self.chat}"
