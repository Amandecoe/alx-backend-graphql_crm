import graphene
import re
#universal database for customers to be stored
Customers = []
added= []
temp_Storage = []
#single customer
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True, unique = True)
        phone = graphene.String(required=False)

    def mutate(self, info, name, phone, email):
            pattern = r"^(\+2519\d{8}|09\d{8})$"
            for c in Customers:
             if c["email"] == email:
              return CreateCustomer(ok=False, customer=None, message = "Email Already Exists")

            if not re.match(pattern, phone):
                return CreateCustomer(ok=False, message = "Invalid phone number format")
            else:
                msg = f"Customer {name} with phone number {phone} created!"
                return CreateCustomer(ok=True, message=msg)
            
#Bulk part
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False)   
class BulkCreateCustomer(graphene.Mutation):
    class Arguments:
        customers = graphene.List(CustomerInput, required=True)

    ok = graphene.Boolean()
    #indicates if the mutation succeeded or failed
    added_customers = graphene.List(CustomerInput)
    #Returns the customers that were actually added with their fields
    message = graphene.String()
    #provides a human readable explanation of what happened

    def mutate(self, info, customers):
        temp_storage = []

        for c in customers:
            # validate phone if provided
            if c.phone and not re.match(r"^(\+2519\d{8}|09\d{8})$", c.phone):
                return BulkCreateCustomer(ok=False, added_customers=None, message=f"Invalid phone: {c.phone}")

            # check duplicate email
            if any(existing["email"] == c.email for existing in Customers):
                return BulkCreateCustomer(ok=False, added_customers=None, message=f"Duplicate email: {c.email}")

            temp_storage.append({"name": c.name, "email": c.email, "phone": c.phone})

        # commit all
        Customers.extend(temp_storage)
        added_customers = [CustomerInput(**c) for c in temp_storage] #double * unpacks dictionary into keyword arguments, the ones put in temp_storage

        return BulkCreateCustomer(ok=True, added_customers=added_customers, message = "All customers added successfuly")
             
          