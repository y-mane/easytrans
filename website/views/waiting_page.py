from multiprocessing import context
from django.shortcuts import render,redirect
from start_form.models import Compagnie, Voyage,Montant,Agence
from start_form.forms import VoyageForm
from django.template.defaulttags import register
import requests
from django.views.decorators.http import require_http_methods



@register.filter
def get_item(dict,key):
    
    return dict.get(key)

@require_http_methods(["GET","POST"])
def waiting_page(request,last_id):
    voyage=Voyage.objects.get(id=last_id)
    depart=voyage.lieu_depart
    destination=voyage.destination
    montant=Montant.objects.get(depart=depart,destination=destination)
    prix=montant.prix
            
    context={
        'voyage':voyage,
        'prix':prix,
        'last_id':last_id
        }
    return render(request,'website/front/waiting_page.html',context) 

