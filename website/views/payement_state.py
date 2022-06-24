from urllib import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
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

"""@api_view(['GET']) 
@parser_classes((JSONParser,)) 
def example_view(request, format=None):
    return Response({'custom_data': request.data})"""

@api_view(['POST'])
def notification(request):
    custom_data=request.data 
    if custom_data: 
        voyage=Voyage.objects.get(id=custom_data)
        return Response(voyage)
    else:
        return Response({'details':'custom_data not exist'})
    #voyage.etat_paiement=Voyage.ETAT_PAIEMENT[0][0]
    
    #return render(request,'website/front/notification.html',context)