from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Compagnie)
admin.site.register(Ville)
admin.site.register(Commune)
admin.site.register(Agence)
admin.site.register(Voyage)
admin.site.register(Mission)
admin.site.register(Ticket)
admin.site.register(Montant)
admin.site.register(Signature)