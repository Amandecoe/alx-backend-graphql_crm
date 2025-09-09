import graphene
import re

Customers = []

class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.EmailField(required=True, unique = True)
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
#list of the customerinputs
#           