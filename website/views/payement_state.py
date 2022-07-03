from urllib import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
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
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def success(request):
    context={
    }
    return render(request,'website/front/success.html',context)

@require_http_methods(["POST"])
def failled(request):
    context={        
    }
    return render(request,'website/front/failled.html',context)



@api_view(['POST'])
def notification(request):
    var = dict()
    var={k:v for k,v in request.POST.items()}
    #print(request.POST['customer'])
    customer=var['customer']
    print(customer)
    custom_data=var['extra_data']
    print(custom_data)
    voyage_id=int(custom_data)
    payement_state=var['txn_status']
    print(payement_state)
    if payement_state=='success':
        voyage=Voyage.objects.get(id=voyage_id)
        voyage.etat_paiement=Voyage.ETAT_PAIEMENT[0][0]
        voyage.save()
        voy=model_to_dict(voyage)
        print(voy)
        #API pour envoyer les sms
        """conn = http.client.HTTPConnection("vavasms.com")
        payload = "username=keita.souleyman225@gmail.com&password=thelifeislesgigas2020&sender_id=keita&phone={voyage.contact}&message=paiment effectué avec succès"
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
            return Response({'details':'payement non éffectué '})
    