import requests

endpoint = ""
response = requests.post(endpoint, json={'custom_data':"10#success"})
print(response.json())
print(response.status_code)