from distutils.log import debug
from urllib import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import json
import pprint
import requests
from multiprocessing import context
from django.shortcuts import render,redirect
from start_form.models import Voyage,Compagnie,Agence,Signature
from start_form.forms import VoyageForm
from django.forms.models import model_to_dict
import http.client
import mimetypes
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import  require_POST
import logging 


log = logging.getLogger('debug')

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
    var = dict()
    var={k:v for k,v in request.data.items()}
    signature=var['signature']
    custom_data=var['extra_data']
    voyage_id=int(custom_data or 0)
    payement_state=var['txn_status']
    try:
        signature_obj=Signature.objects.get(signature=signature)
        return Response({'details':'notification déjà envoyé'})
    except:
        if payement_state=='success' or payement_state=='successful':
            log.info(f"[notification de paiement]:information recuperee:{request.POST.items()}")
            sign=Signature.objects.create(signature=signature)
            sign.save()
            voyage=Voyage.objects.get(id=voyage_id)
            voyage.etat_paiement=Voyage.ETAT_PAIEMENT[0][0]
            voyage.save()
            voy=model_to_dict(voyage)
            #API pour envoyer les sms
            """conn = http.client.HTTPConnection("vavasms.com")
            payload = "username=keita.souleyman225@gmail.com&password=thelifeislesgigas2020&sender_id=keita&phone={{voyage.contact}}&message=paiment effectué avec succès"
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
            return Response(voy or 0) 
        else:
            return Response({'details':'notification déjà recu'})
