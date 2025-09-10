import graphene
import re

class CustomerType(graphene.ObjectType): #output
     id = graphene.ID()
     name = graphene.String(required=True)
     email = graphene.String(required = True)
     phone = graphene.String()
class CreateCustomer(graphene.Mutation):
    class Arguments:  #input
       name = graphene.String(required=True)
       email = graphene.String(required=True)
       phone = graphene.String()
    def mutate(self, root, info, phone, name,email):
        customer = graphene.Field(CustomerType)
        message = graphene.String()
        new_id = len(customer)+1
        pattern = r"^(\+2519\d{8}|09\d{8})$"
        if not re.match(pattern, customer.phone):
            return CreateCustomer(ok=False, customer=None, message= "Invalid phone format")

        customer = {"id": new_id, "name": name, "email":email, "phone":phone}
        return CreateCustomer(ok=True, customer=CustomerType(**customer), messagae="Customer created successfully")
        #the ** expands the dictionary into keyword arguments when displayed