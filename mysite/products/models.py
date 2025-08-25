from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=200, help_text="Category name")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    # Character fields
    name = models.CharField(max_length=200, db_index=True)
    sku = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    # Text fields
    description = models.TextField(blank=True)
    specifications = models.JSONField(null=True, blank=True)
    
    # Numeric fields
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    
    # Date and time fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    release_date = models.DateField(null=True, blank=True)
    
    # File fields
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    manual_pdf = models.FileField(upload_to='manuals/', blank=True)
    
    # Relationship fields
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    related_products = models.ManyToManyField('self', blank=True)
    
    # Choice fields
    AVAILABILITY_CHOICES = [
        ('IN', 'In Stock'),
        ('OT', 'Out of Stock'),
        ('PR', 'Pre-order'),
    ]
    availability = models.CharField(
        max_length=2,
        choices=AVAILABILITY_CHOICES,
        default='IN'
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['created']),
        ]
        
    def __str__(self):
        return self.name
        
    @property
    def discounted_price(self):
        if self.discount_percent > 0:
            return self.price * (1 - self.discount_percent / 100)
        return self.price

class ProductReview(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f'Review by {self.author} on {self.product}'
