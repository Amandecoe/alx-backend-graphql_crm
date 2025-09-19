import django_filters
from .models import Customer, Product, Order

class Customerfilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    phone = django_filters.CharFilter(method="filter_phone")

    class Meta:
        model = Customer
        fields = ["name", "email", "phone"]  # only actual model fields

    def filter_phone(self, queryset, name, value):
        return queryset.filter(phone__startswith=value)


class Productfilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    price = django_filters.RangeFilter(field_name="price")
    stock = django_filters.RangeFilter(field_name="stock")
    low_stock = django_filters.NumberFilter(method="filter_low_stock")

    class Meta:
        model = Product
        fields = ["name", "price", "stock"]

    def filter_low_stock(self, queryset, name, value):
        return queryset.filter(stock__lt=10)


class Orderfilter(django_filters.FilterSet):
    total_amount = django_filters.RangeFilter(field_name="total_amount")
    order_date = django_filters.DateFromToRangeFilter(field_name="order_date")
    customer_name = django_filters.CharFilter(field_name="customer__name", lookup_expr="icontains")
    product_name = django_filters.CharFilter(method="filter_product_name")
    product_id = django_filters.NumberFilter(method="filter_product_id")

    class Meta:
        model = Order
        fields = ["total_amount", "order_date", "customer"]

    def filter_product_name(self, queryset, name, value):
        return queryset.filter(product__name__icontains=value)

    def filter_product_id(self, queryset, name, value):
        return queryset.filter(product__id=value)