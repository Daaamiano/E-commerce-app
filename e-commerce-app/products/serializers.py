from rest_framework import serializers
from .models import Role, Product, Order, OrderItem, ProductCategory
from PIL import Image
import datetime

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Role.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category', 'image', 'thumbnail')

    def validate_image(self, value):
        if value:
            try:
                # Odczytaj obraz za pomocą Pillow
                img = Image.open(value)
                width, height = img.size

                # Sprawdź, czy szerokość jest większa niż 200px
                if width < 200:
                    raise serializers.ValidationError('Szerokość obrazu musi być większa niż 200px.')

            except AttributeError:
                # Jeśli obraz nie jest poprawny
                raise serializers.ValidationError('Nieprawidłowy format obrazu.')

        return value


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')

class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'client', 'delivery_address', 'orderitem_set')

    def create(self, validated_data):
        products_data = validated_data.pop('orderitem_set')
        payment_due_date = datetime.datetime.now() + datetime.timedelta(days=5)
        order = Order.objects.create(payment_due_date=payment_due_date, **validated_data)
        order.total_price = sum(item.get("product").price * item.get("quantity") for item in products_data)

        for product_data in products_data:
            OrderItem.objects.create(order=order, product=product_data.get("product"), quantity=product_data.get("quantity"))

        return order

class TopProductsSerializer(serializers.Serializer):
    product__name = serializers.CharField()
    total_quantity = serializers.IntegerField()