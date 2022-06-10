from multiprocessing import context
from django.shortcuts import render,redirect
from start_form.models import Compagnie, Voyage,Montant,Agence
from start_form.forms import VoyageForm
from django.template.defaulttags import register
import requests
import http.client
import mimetypes



@register.filter
def get_item(dict,key):
    
    return dict.get(key)


def waiting_page(request,last_id):
    voyage=Voyage.objects.get(id=last_id)
    depart=voyage.lieu_depart
    destination=voyage.destination
    montant=Montant.objects.get(depart=depart,destination=destination)
    prix=montant.prix
    
    """if request.method=='POST':      
        #API pour envoyer les sms
            conn = http.client.HTTPConnection("vavasms.com")
            payload = "username=keita.souleyman225@gmail.com&password=thelifeislesgigas2020&sender_id=keita.souleyman225@gmail.com&phone=+2250708176279&message=bonjour"
            headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Accept': "*/*",
            'Host': "vavasms.com"
            }
            conn.request("POST", "api,v1,text,single", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
            #fin API d'envoie de sms """
    context={
        'voyage':voyage,
        'prix':prix,
        'last_id':last_id
        }
    return render(request,'website/front/waiting_page.html',context) 

