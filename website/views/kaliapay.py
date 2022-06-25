import requests


endpoint = "http://146.190.238.183:80/payement_state/notification/"
response = requests.post(endpoint, json={'custom_data':"1#success"})
print(response.json())
print(response.status_code)