import requests


endpoint = "http://146.190.238.183/payement_state/notification/"
response = requests.post(endpoint, json={'custom_data':"1#success"})
print(response)
print(response.status_code)