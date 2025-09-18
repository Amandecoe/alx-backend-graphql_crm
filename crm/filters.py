from .models import Customer, Product, Order
import django_filters
# icontains looks up for a field, i = case-insensetive and contains verifies if it contains
class Customerfilter(django_filters.Filterset):
    name_contains = django_filters.CharFilter(
        field_name = "name", lookup_Expr = "icontains"
    )
    email_contains = django_filters.CharFilter(
        field_name = "email", lookup_Expr = "icontains"
    )
    created_at_contains = django_filters.DateFilter(
        field_name = "created_at", lookup_Expr = "gte"
    )
    phone_startwith = django_filters.CharFilter(method = "phone_number_startswith")
    
    class meta:
        model = Customer
        Fields = ["name", "email", "created_at"]

    def phone_number_startswith(self, queryset, name, value):
        return queryset.filter(phone_startwith = +1) 

            

class Productfilter(django_filters.Filterset):
    name_contains = django_filters.CharFilter(
        field_name = "name", lookup_Expr = "icontains"
    )       
    price_contains = django_filters.RangeFilter(
        field_name = "price", lookup_Expr = "gte"  #gte stands for greater than or equal to
    )
    stock_contains = django_filters.RangeFilter(
        field_name = "stock", lookup_Expr = "gte"
    )
    low_stock_products = django_filters.NumberFilter (method = "product_with_low_Stock") #products with stock less than 10
    
    class meta:
        model = Product
        Fields = ["name", "price", "stock"]

    def product_with_low_Stock(self, queryset, name, value):
        return queryset.filter(stock_lt = 10)

class OrderFilter(django_filters.Filterset):
    total_amount_contains = django_filters.RangeFilter(
        field_name = total_amount, lookup_Expr = "gte"
    )        
    order_date_contains = django_filters.DateFilter(
        field_name = order_date, lookup_Expr = "gte"
    )
    customer_name_contains = django_filters.CharFilter(
        field_name = customer, lookup_Expr = "icontains"
    )
    products_name_contains = django.filters.CharFilter(
        field_name = product, lookup_Expr = "icontains"
    )
    product_id = django.filter.NumberFilter(method = "filter_by_product")

    def filter_by_product():
        return queryset.Filter (products_id=2)
    class meta:
        model = Order
        Fields = ["total_amount", "order_date", "customer"]