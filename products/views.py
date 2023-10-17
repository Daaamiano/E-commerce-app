from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from .models import Role, Product, Order, OrderItem
from .serializers import CustomUserSerializer, ProductSerializer, OrderItemSerializer, OrderSerializer, TopProductsSerializer, ProductCategorySerializer
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCustomer, IsSeller
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from django.core.mail import send_mail
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils.html import strip_tags
from .forms import LoginForm
from rest_framework.response import Response

class UserRegistrationView(generics.CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class UserLoginView(LoginView):
    def login_view(request):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                role = form.cleaned_data['role']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if role == user.role:
                        login(request, user)
                        return redirect('/products/')  # Przekierowanie do odpowiedniej strony po zalogowaniu
                    else:
                        # Nieprawidłowa rola dla użytkownika
                        return render(request, 'login.html', {'form': form, 'error_message': 'Nieprawidłowa rola.'})
                else:
                    # Nieprawidłowe dane logowania
                    return render(request, 'login.html', {'form': form, 'error_message': 'Nieprawidłowe dane logowania.'})
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'category__name', 'description']
    ordering_fields = ['name', 'category__name', 'price']
    pagination_class = PageNumberPagination

class ProductCategoryCreateView(generics.CreateAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated, IsSeller]
    parser_classes = (MultiPartParser, FormParser)

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    parser_classes = (MultiPartParser, FormParser)

class ProductUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    parser_classes = (MultiPartParser, FormParser)

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def perform_create(self, serializer):
        order = serializer.save(client=self.request.user)
        order.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        order = serializer.instance
        
        response_data = {
            'order_id': order.id,
            'total_price': order.total_price,
            'payment_due_date': order.payment_due_date
        }
        subject = 'Potwierdzenie zamówienia'
        message = 'Dziękujemy za złożenie zamówienia. Twój numer zamówienia to {}'.format(order.id)
        from_email = 'noreply@example.com'
        recipient_list = [self.request.user.email]

        send_mail(subject, strip_tags(message), from_email, recipient_list, html_message=message)
        
        return Response(response_data, status=status.HTTP_201_CREATED)

class TopProductsView(generics.ListAPIView):
    serializer_class = TopProductsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        num_products = self.request.query_params.get('num_products', 10)
        queryset = OrderItem.objects.filter(order__order_date__gte=start_date, order__order_date__lte=end_date) \
            .values('product__name') \
            .annotate(total_quantity=Count('product')) \
            .order_by('-total_quantity')[:int(num_products)]

        return queryset
