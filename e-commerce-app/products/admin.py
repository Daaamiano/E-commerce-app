from django.contrib import admin
from .models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'category', 'image', 'thumbnail')

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'delivery_address', 'total_price', 'payment_due_date')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('role',)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Role, RoleAdmin)