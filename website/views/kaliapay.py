import requests

endpoint = "http://146.190.238.183/payement_state/notification/"
response = requests.post(endpoint, json={2})
print(response.json)
print(response.status_code)