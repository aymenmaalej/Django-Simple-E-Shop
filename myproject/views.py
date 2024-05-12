from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    context={'val':"Menu Acceuil"} 
    return render(request,'mesProduits.html',context)

def index(request):
    return render(request,'acceuil.html' )