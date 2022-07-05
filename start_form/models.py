from logging import PlaceHolder
from random import choices
from unicodedata import name
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
#from compte.models import User
    

# Create your models here.
class Compagnie(models.Model):
    name=models.CharField(max_length=250)
    description=models.TextField()
    reference=models.CharField(max_length=250)
    contact1=models.CharField(max_length=250)
    contact2=models.CharField(max_length=250)
    
    def __str__(self):
        return self.name
    
class Ville(models.Model):
    name=models.CharField(max_length=250)
    description=models.TextField()
    reference=models.CharField(max_length=250)
    
    def __str__(self):
            return self.name
    
    
class Commune(models.Model):
    ville=models.ForeignKey(Ville,on_delete=models.CASCADE)
    name=models.CharField(max_length=250)
    description=models.TextField()
    reference=models.CharField(max_length=250)
    
    def __str__(self):
        return self.name
    
    
class Agence(models.Model):
    compagnie=models.ForeignKey(Compagnie,on_delete=models.CASCADE)
    commune=models.ForeignKey(Commune,on_delete=models.CASCADE)
    coordonnee_geo=models.CharField(max_length=300)
    adresse_geo=models.CharField(max_length=300)
    
    def __str__(self):
        return (str(self.compagnie)+'-'+str(self.commune))    
    
    
    
class Voyage(models.Model):
    PERIODE=(
        ('matinée','matinée'),
        ('soirée','soirée')
    )
    STATUT=(
        ('validée','validée'),
        ('échouée','échouée'),
        ('en attente','en attente')
    )
    ETAT=(
        ('en cours','en cours'),
        ('achevé','achevé')
    )
    ETAT_PAIEMENT=(('succes','succes'),
                   ('echec','echec')
    )
    fullname=models.CharField(max_length=250)
    contact=models.CharField(max_length=250)
    email=models.EmailField(blank=True)
    compagnie=models.ForeignKey(Compagnie,on_delete=models.CASCADE)
    lieu_depart=models.ForeignKey(Agence,on_delete=models.CASCADE,related_name='lieu_depart')
    destination=models.ForeignKey(Agence,on_delete=models.CASCADE,related_name='destination')
    periode=models.CharField(max_length=250,choices=PERIODE)
    lieu_livraison=models.CharField(max_length=250)
    statut_commande=models.CharField(max_length=250,choices=STATUT,blank=True,default='en attente')
    date_heure_commande=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    date_heure_traitement=models.DateTimeField(auto_now=True,blank=True,null=True)
    date_heure_succces=models.DateTimeField(auto_now=True,blank=True,null=True)
    etat_voyage=models.CharField(max_length=250,choices=ETAT,blank=True,default='en cours')
    reference=models.CharField(max_length=250,blank=True)
    etat_paiement=models.CharField(max_length=250,choices=ETAT_PAIEMENT,default='echec', blank=True,null=True)
    
    def __str__(self):
        return self.fullname  

class Mission(models.Model):
    livreur=models.ForeignKey(User,related_name='livreur',on_delete=models.DO_NOTHING)      
    voyage=models.ForeignKey(Voyage,on_delete=models.CASCADE)
    #heure_recuperation=models.TimeField(blank=True)
    #heure_livraison=models.TimeField(blank=True)
    commentaire=models.TextField(blank=True)
    
    def __str__(self):
        return ('Client:  '+str(self.voyage))
    
    
    
    
    
    #user=models.ForeignKey(User,on_delete=models.CASCADE)

class Ticket(models.Model):
    voyage=models.ForeignKey(Voyage,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='image',blank=True)
    reference=models.CharField(max_length=250)
    description=models.TextField(blank=True)
    visa_client=models.TextField()
    
    def __str__(self):
        return str(self.voyage)
    
class Montant(models.Model):
        compagnie=models.ForeignKey(Compagnie,on_delete=models.DO_NOTHING)
        depart=models.ForeignKey(Agence,on_delete=models.DO_NOTHING,related_name='depart')
        destination=models.ForeignKey(Agence,on_delete=models.DO_NOTHING,related_name='desti')
        prix=models.CharField(max_length=250)
        
        def __str__(self):
            return (str(self.depart)+'===>'+str(self.destination)+':'+str(self.prix)+'FCFA')
    

class Signature(models.Model):
    signature=models.CharField(max_length=250)
    
    def __str__(self):
        return self.signature