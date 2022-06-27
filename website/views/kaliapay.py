import requests

endpoint = "http://127.0.0.1:8000/payement_state/notification/"

#response = requests.get(endpoint)
response = requests.post(endpoint, json={'custom_data':"3#success"})
print(response.json())
print(response.status_code)