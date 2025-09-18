from .models import Customer, Product, Order

class Customerfilter(django_filters.Filterset):
    name_contains = django_filters.CharFilter(
        field_name = "name", lookup_Expr = "icontains"
    )
    email_contains = django_filters.CharFilter(
        field_name = "email", lookup_Expr = "icontains"
    )
    created_at = django_filters.DateFilter(
        field_name = "created_at", lookup_Expr = "gte"
    )