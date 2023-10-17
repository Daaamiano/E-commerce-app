from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import User, AbstractUser
from e_commerce_app.settings import AUTH_USER_MODEL

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    thumbnail = models.ImageField(upload_to='products/thumbnails/')

    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    delivery_address = models.TextField()
    products = models.ManyToManyField(Product, through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)
    payment_due_date = models.DateTimeField(null=True)
    total_price = models.DecimalField(null=True, max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order #{self.pk} by {self.client.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity}x {self.product.name} in Order #{self.order.pk}'
    
class Role(AbstractUser):
    ROLE_CHOICES = (
        ('Klient', 'Klient'),
        ('Sprzedawca', 'Sprzedawca'),
    )
    # REQUIRED_FIELDS = ('role',)


    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Klient')

    def __str__(self):
        return self.username