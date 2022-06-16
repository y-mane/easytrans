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
    #if request.method=='POST':
    custom_data=request.POST.get('custom_data')
    print(custom_data)
    voyage=Voyage.objects.get(id=custom_data)
    voyage.etat_paiement=Voyage.ETAT_PAIEMENT[0][0]
    context={
        
        
    }
    return render(request,'website/front/notification.html')