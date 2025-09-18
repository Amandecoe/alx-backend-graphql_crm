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
    
    def product_with_low_Stock(self, queryset, name, value):
        return queryset.filter(stock_lt = 10)