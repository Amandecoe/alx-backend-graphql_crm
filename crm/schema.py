import graphene
import re
import seed_db
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
        #checks for phone format 
        if not re.match(pattern, customer.phone):
            return CreateCustomer(ok=False, customer=None, message= "Invalid phone format")
        #checks for duplicate email
        if any(c["email"] == email for c in customer):
            return CreateCustomer(ok=False, customer=None, message="Email Already Exists")
        
        customer_data = seed_db.add_customer(name, email, phone)
        return CreateCustomer(ok=True, customer=CustomerType(**customer), messagae="Customer created successfully")
        #the ** expands the dictionary into keyword arguments when displayed

