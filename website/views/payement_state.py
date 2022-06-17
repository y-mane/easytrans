import pprint
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

def notification(request):
    custom_data=5
    voyage=Voyage.objects.get(id=custom_data)
    voyage.etat_paiement=Voyage.ETAT_PAIEMENT[0][0]
    context={
        'custom_data':custom_data
        
    }
    return render(request,'website/front/notification.html',context)