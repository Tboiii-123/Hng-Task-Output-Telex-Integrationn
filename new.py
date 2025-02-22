import requests

url="https://ping.telex.im/v1/webhooks/01952cec-d6ed-749a-8300-89efa1c8f8d7"
payload = {
    "event_name": "string",
    "message": "python @post",
    "status": "success",
    "username": "Tboiii"
}

response = requests.post(
    url,
    json=payload,
    headers={
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
)
print(response.json())
