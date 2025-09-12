import graphene
import re
import seed_db


# Output type
class CustomerType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


# Error type
class CustomerError(graphene.ObjectType):
    name = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    message = graphene.String()


# Input type (for bulk mutation)
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class ProductType(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock = graphene.Int(required = False, default = 0)

# Single customer creation
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    ok = graphene.Boolean()
    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        customers = seed_db.get_customers()

        # Phone validation
        if phone:
            pattern = r"^(\+2519\d{8}|09\d{8})$"
            if not re.match(pattern, phone):
                return CreateCustomer(ok=False, customer=None, message="Invalid phone format")

        # Duplicate email check
        if any(c["email"] == email for c in customers):
            return CreateCustomer(ok=False, customer=None, message="Email already exists")

        # Save to seed_db
        customer_data = seed_db.add_customer(name, email, phone)

        return CreateCustomer(
            ok=True,
            customer=CustomerType(**customer_data),
            message="Customer created successfully"
        )


# Bulk customer creation
class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(CustomerInput, required=True)

    created = graphene.List(CustomerType)
    errors = graphene.List(CustomerError)

    def mutate(self, info, customers):
        created_customers = []
        errors = []

        existing = seed_db.get_customers()

        for cust in customers:
            name, email, phone = cust.name, cust.email, cust.phone

            # Phone validation
            if phone:
                pattern = r"^(\+2519\d{8}|09\d{8})$"
                if not re.match(pattern, phone):
                    errors.append(CustomerError(
                        name=name,
                        email=email,
                        phone=phone,
                        message="Invalid phone format"
                    ))
                    continue

            # Duplicate email check (existing + newly added in this mutation)
            if any(c["email"] == email for c in existing + [c.__dict__ for c in created_customers]):
                errors.append(CustomerError(
                    name=name,
                    email=email,
                    phone=phone,
                    message="Email already exists"
                ))
                continue

            # Add to DB + created list
            customer_data = seed_db.add_customer(name, email, phone)
            created_customers.append(CustomerType(**customer_data))

        return BulkCreateCustomers(created=created_customers, errors=errors)

class CreateProduct(graphene.Mutation):
    class Arguments:
      name = graphene.String(required=True)
      price = graphene.Decimal(required=True)
      stock = graphene.Int(required=True, default = 0 )
      Product = graphene.List(ProductType)
      def mutate(self, info, name, price,stock, Product):
          for p in Product:
              if p.price<0 :
                  return "Price Can Not be Negative"
              if p.stock < 0 :
                  return "Stock can not be Negative"

          customer_data = seed_db.add_product(name, price, stock)
          Product.append(ProductType(**customer_data))   

          return CreateProduct(created = Product, Message = "Product created successfully")   