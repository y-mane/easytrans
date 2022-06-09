from multiprocessing import context
from django.shortcuts import render,redirect
from start_form.models import Voyage,Compagnie,Agence
from start_form.forms import VoyageForm



def success(request):
    
    context={
        
    }
    return render(request,'website/front/success.html',context)

def failled(request,form):
    
    context={
        'form':form
    }
    return render(request,'website/front/failled.html',context)

def notification(request):
    """print(form.fullname)
    context={
        'voyage':form
    }"""
    return render(request,'website/front/notification.html')