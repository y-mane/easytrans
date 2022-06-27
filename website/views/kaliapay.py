import requests

endpoint = "http://127.0.0.1:8000/payement_state/notification/"

#response = requests.get(endpoint)
response = requests.post(endpoint, json={'extra_data':3,'txn_status':'success'})
print(response.json())
print(response.status_code)