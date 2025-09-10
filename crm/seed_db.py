import json #so that we can store python dictionaries in a file as JSON
import os #checks if the database file already exists

DB_FILE = "db.json" #is the name of the file that will hold our database, this is where everything is saved

if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        data = json.load(f)
else:
    data = {"customers": [], "products": [], "orders": []}    #if the file exists it will open it in "r"(Read) mode and loads the json into a python dictionary called data,
    #if the file does not exist it creates an empty structure with 3 lists 

_next_customer_id = len(data["customers"])+1
_next_product_id = len(data["products"])+1
_next_order_id = len(data["orders"])+1
#these keep track of the next ID to assign when creating a new customer/product/order

def save_db():
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)
#this opens the database file DB_FILE in write mode and dumps the data dictionary into the file with 2 indentations for readability

def add_customer(name, email, phone):
    global _next_customer_id
#defines a function to insert a new customer into the database, the _next_customer_id ensures we modify the global counter instead of creating a local copy
    customer = {                
        "id": str(_next_customer_id),
        "name": name,
        "email": email,
        "phone": phone,
    }
    data["customers"].append(customer)
    _next_customer_id += 1
    save_db()
    return customer              

def get_all_customers():
    return data["customers"]