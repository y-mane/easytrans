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


def waiting_page(request):
    #voyage=Voyage.objects.get(id=last_id)
    fullname=request.POST.get('fullname')
    contact=request.POST.get('contact')
    lieu_livraison=request.POST.get('lieu_livraison')
    compagnie=request.POST.get('compagnie')
    compagnie_name=Compagnie.objects.get(id=compagnie)
    depart=request.POST.get('lieu_depart')
    lieu_depart=Agence.objects.get(id=depart)
    desti=request.POST.get('destination')
    destination=Agence.objects.get(id=desti)
    periode=request.POST.get('periode')
    montant=Montant.objects.get(depart=depart,destination=destination)
    prix=montant.prix
    voyage={
        'fullname':fullname,
        'contact':contact,
        'lieu_livraison':lieu_livraison,
        'compagnie':compagnie_name,
        'lieu_depart':lieu_depart,
        'destination':destination,
        'periode':periode
        
    }
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
        }
    return render(request,'website/front/waiting_page.html',context) 

