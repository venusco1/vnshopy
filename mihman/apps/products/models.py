from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField


class Category(models.Model):
    cat_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)  # For URL-friendly representation
    description = models.TextField(max_length=250, blank=True)
    cat_img = models.ImageField(upload_to="photos/categories", blank=True, null=True)

    def __str__(self):
        return self.cat_name


class Subcategory(models.Model):
    subcat_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100, unique=True)  # For URL-friendly representation
    description = models.TextField(max_length=200, blank=True)
    subcat_img = models.ImageField(upload_to="photos/subcategories", blank=True, null=True)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.subcat_name

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    product_image = models.ImageField(upload_to="photos/categories", blank=True, null=True)
    # images = ArrayField(models.CharField(max_length=200), blank=True, default=list)  # Store image paths
    
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    warranty_period = models.CharField(max_length=100, blank=True)  # Warranty info

    # Relationships with Category and Subcategory
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, blank=True, null=True)
    subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.CASCADE, blank=True, null=True)

    # Product specifications
    size = models.CharField(max_length=10, blank=True)  # e.g., Small, Medium, Large
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  # Weight in kilograms (kg)
    dimensions = models.CharField(max_length=50, blank=True)  # e.g., 10x5x3 cm or 20x20x5 inches
    material = models.CharField(max_length=100, blank=True)  # Material information, e.g., Cotton, Steel
    color = models.CharField(max_length=50, blank=True)  # Single color
    
    
    # Wishlist
    wishlisted_by = models.ManyToManyField(User, related_name='wishlisted_products', blank=True)
    
    # e.g., Made in China, USA
    country_of_origin = models.CharField(max_length=100, blank=True)  

    # Reviews and Ratings
    total_reviews = models.IntegerField(default=0)
    total_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    # Cart and Buy Now functionality
    cart_users = models.ManyToManyField(User, related_name='cart_products', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        self.is_available = self.stock > 0
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    # Method to calculate discounted price if applicable
    def get_final_price(self):
        if self.discount_percentage:
            discount_amount = (self.price * self.discount_percentage) / 100
            return self.price - discount_amount
        return self.price

    # Method to update ratings
    def update_rating(self, new_rating):
        if self.total_reviews == 0:
            self.total_rating = new_rating
        else:
            self.total_rating = ((self.total_rating * self.total_reviews) + new_rating) / (self.total_reviews + 1)
        self.total_reviews += 1
        self.save()

    # Method to add a product to a user's wishlist
    def add_to_wishlist(self, user):
        self.wishlisted_by.add(user)
        self.save()

    # Method to remove a product from a user's wishlist
    def remove_from_wishlist(self, user):
        self.wishlisted_by.remove(user)
        self.save()

    # Method to add a product to the cart
    def add_to_cart(self, user):
        self.cart_users.add(user)
        self.save()

    # Method to remove a product from the cart
    def remove_from_cart(self, user):
        self.cart_users.remove(user)
        self.save()