from audioop import reverse
from multiprocessing import context
from django.shortcuts import render,redirect
from start_form.models import Voyage,Compagnie,Agence
from start_form.forms import VoyageForm
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import requests
import http.client
import mimetypes


def frontspace(request):
    form=VoyageForm()
    if request.method=='POST' :
        form=VoyageForm(request.POST)
        if form.is_valid():
            form.save()
            #last_id=Voyage.objects.latest('id').id
            return redirect('success',form)
      
    context={
        'form':form,
    }
    return render (request,'website/front/frontspace.html',context)



def load_agence(request):
    compagnie_id = request.GET.get('compagnie_id')
    lieu_depart = Agence.objects.filter(compagnie_id=compagnie_id).all()
    context={
        'lieu_depart': lieu_depart,
    }
    return render(request, 'website/front/depart_dropdown_list_options.html',context)
    #return JsonResponse(list(gars.values('id', 'name')), safe=False)
     
def load_destination(request):
    compagnie_id = request.GET.get('compagnie_id')
    destination=Agence.objects.filter(compagnie_id=compagnie_id).all()
    context={
        'destination':destination
    }
    return render(request, 'website/front/destination_dropdown_list_options.html',context)


