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
from django.forms.models import model_to_dict
import http.client
import mimetypes


def success(request):
    context={
    }
    return render(request,'website/front/success.html',context)

def failled(request):
    context={        
    }
    return render(request,'website/front/failled.html',context)


@api_view(['POST'])
def notification(request):
    custom_data=request.data["custom_data"]
    custom=custom_data.split("#")
    voyage_id=int(custom[0])
    payement_state=custom[1]
    if payement_state=='success': 
        voyage=Voyage.objects.get(id=voyage_id)
        voyage.etat_paiement=Voyage.ETAT_PAIEMENT[0][0]
        voyage.save()
        voy=model_to_dict(voyage)
        #API pour envoyer les sms
        """conn = http.client.HTTPConnection("vavasms.com")
        payload = "username=keita.souleyman225@gmail.com&password=thelifeislesgigas2020&sender_id=keita.souleyman225@gmail.com&phone={voyage.contact}&message=paiment effectué avec succès"
        headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Host': "vavasms.com"
        }
        conn.request("POST", "api,v1,text,single", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))"""
        #fin API d'envoie de sms
        return Response(voy) 
    else:
            return Response({'details':'custom_data not exist'})
    