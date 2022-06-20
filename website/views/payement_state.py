from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
import pprint
import requests
from multiprocessing import context
from django.shortcuts import render,redirect
from start_form.models import Voyage,Compagnie,Agence
from start_form.forms import VoyageForm



def success(request):
    context={
    }
    return render(request,'website/front/success.html',context)

def failled(request):
    context={        
    }
    return render(request,'website/front/failled.html',context)

@api_view(['POST']) 
@parser_classes((JSONParser,)) 
def example_view(request, format=None):
    return Response({'custom_data': request.data})

def notification(request):
    custom_data=example_view(request).json
    voyage=Voyage.objects.get(id=custom_data)
    voyage.etat_paiement=Voyage.ETAT_PAIEMENT[0][0]
    
    context={
        'custom_data':custom_data
        
    }
    return render(request,'website/front/notification.html',context)