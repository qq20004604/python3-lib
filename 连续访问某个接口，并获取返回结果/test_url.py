import requests
import json
from time import time

url = "http://127.0.0.1:7001/bbs/login"
n = 100

data = {
    "account": "admin",
    "password": "12345678"
}

headers = {
    "Content-Type": "application/json"
}

total_time = 0

for i in range(n):
    start_time = time()
    response = requests.post(url, data=json.dumps(data), headers=headers)
    response_time = time() - start_time
    total_time += response_time
    response_json = response.json()

    print(f"Request {i + 1}: {response_time}s")
    print("Response body:")
    print(json.dumps(response_json, indent=2))

average_time = total_time / n
print(f"Average response time: {average_time}s")
