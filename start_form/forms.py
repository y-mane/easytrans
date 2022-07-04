from pyexpat import model
from django.forms import ModelForm
from django import forms
from .models import *
#from .models import Post

class VoyageForm(forms.ModelForm):
    class Meta:
        model=Voyage
        fields=['fullname','contact','compagnie','lieu_depart','destination','periode','lieu_livraison','statut_commande']
        #compagnie=forms.ChoiceField(help_text='compagnie')
        widgets={
           'fullname':forms.TextInput(attrs={'placeholder':'votre nom complet','name':'fullname','class':'name agileits','required':''}),
            'contact':forms.TextInput(attrs={'placeholder':'votre contact','class':'contact','required':'','name':'contact','type':'text','minlength':'10','maxlength':'10'}),
            'lieu_livraison':forms.TextInput(attrs={'placeholder':'lieu de livraison','class':'name agileits','required':'','name':'lieu_livraison'}),
            'compagnie':forms.Select(attrs={'class':'section_class_agileits sec-left','name':'compagnie','default':''}),
            'lieu_depart':forms.Select(attrs={'class':'section_class_agileits sec-right','name':'lieu_depart'}),
            'destination':forms.Select(attrs={'class':'section_class_agileits sec-right','name':'destination'}),
            'periode':forms.Select(attrs={'class':'section_class_agileits sec-left','name':'periode'}),


        }
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['lieu_depart'].queryset = Agence.objects.none()
            self.fields['destination'].queryset = Agence.objects.none()
            if 'compagnie' in self.data:
                try:
                    compagnie_id = int(self.data.get('compagnie'))
                    self.fields['lieu_depart'].queryset = Agence.objects.filter(compagnie_id=compagnie_id).order_by('name')
                    self.fields['destination'].queryset = Agence.objects.filter(compagnie_id=compagnie_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['lieu_depart'].queryset = self.instance.compagnie.lieu_depart_set.order_by('name')
                self.fields['destination'].queryset = self.instance.compagnie.destination_set.order_by('name')
        
        
        
        
class MissionForm(ModelForm):
    class Meta:
        model=Mission
        fields=['voyage','livreur','commentaire']
        widgets={
            'livreur':forms.Select(attrs={'name':'livreur'}),
             'voyage':forms.Select(attrs={'name':'voyage'}),  
             'commentaire':forms.TextInput(attrs={'style':'width: 538px; height: 118px;'})

        }