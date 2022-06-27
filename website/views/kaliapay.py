import requests
import json
from django.views.decorators.csrf import csrf_exempt

endpoint = "http://146.190.238.183/payement_state/notification/"
response = requests.post(endpoint, json={'custom_data':"3#success"})
print(response.json())
print(response.status_code)