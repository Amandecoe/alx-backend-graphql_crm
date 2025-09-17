import graphene
from graphene_django.types import DjangoObjectType
from django.utils import timezone
from graphql import GraphQLError
from .models import Customer, Product, Order

# --- Types ---
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "stock")


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer", "products", "order_date", "total_amount")


# --- Input Types ---
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock = graphene.Int(required=False, default=0)


# --- Mutations ---
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    ok = graphene.Boolean()
    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if phone and not (phone.startswith("+2519") or phone.startswith("09")):
            return CreateCustomer(ok=False, customer=None, message="Invalid phone format")

        if Customer.objects.filter(email=email).exists():
            return CreateCustomer(ok=False, customer=None, message="Email already exists")

        customer = Customer.objects.create(name=name, email=email, phone=phone)
        return CreateCustomer(ok=True, customer=customer, message="Customer created successfully")


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(CustomerInput, required=True)

    created = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, customers):
        created_customers = []
        errors = []

        for c in customers:
            # Phone validation
            if c.phone and not (c.phone.startswith("+2519") or c.phone.startswith("09")):
                errors.append(f"{c.name}: Invalid phone format")
                continue

            if Customer.objects.filter(email=c.email).exists():
                errors.append(f"{c.name}: Email already exists")
                continue

            customer = Customer.objects.create(name=c.name, email=c.email, phone=c.phone)
            created_customers.append(customer)

        return BulkCreateCustomers(created=created_customers, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int(required=False, default=0)

    ok = graphene.Boolean()
    product = graphene.Field(ProductType)
    message = graphene.String()

    def mutate(self, info, name, price, stock=0):
        if price < 0:
            raise GraphQLError("Price cannot be negative")
        if stock < 0:
            raise GraphQLError("Stock cannot be negative")

        product = Product.objects.create(name=name, price=price, stock=stock)
        return CreateProduct(ok=True, product=product, message="Product created successfully")


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.Int(required=True)
        product_ids = graphene.List(graphene.Int, required=True)
        order_date = graphene.DateTime(required=False)

    ok = graphene.Boolean()
    order = graphene.Field(OrderType)
    message = graphene.String()

    def mutate(self, info, customer_id, product_ids, order_date=None):
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise GraphQLError("Invalid customer ID")

        if not product_ids:
            raise GraphQLError("At least one product must be selected")

        products = Product.objects.filter(pk__in=product_ids)
        if len(products) != len(set(product_ids)):
            raise GraphQLError("One or more product IDs are invalid")

        order = Order(customer=customer, order_date=order_date or timezone.now())
        order.save()
        order.products.set(products)

        total_amount = sum(p.price for p in products)
        order.total_amount = total_amount
        order.save()

        return CreateOrder(ok=True, order=order, message="Order created successfully")


# --- Root Mutation ---
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()