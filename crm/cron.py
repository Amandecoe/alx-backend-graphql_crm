import datetime
import requests

def log_crm_heartbeat():
    log_file = "/tmp/crm_heartbeat_log.txt"
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Base message
    message = f"{now} CRM is alive"

    # Optional GraphQL query to check endpoint
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.ok and "hello" in response.text:
            message += " | GraphQL OK"
        else:
            message += " | GraphQL ERROR"
    except Exception as e:
        message += f" | GraphQL FAIL ({e})"

    # Append to file
    with open(log_file, "a") as f:
        f.write(message + "\n")