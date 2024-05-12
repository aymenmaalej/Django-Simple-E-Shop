from django.shortcuts import render, redirect , get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Produit , Fournisseur , Cart, CartItem , Categorie
from .forms import Fournisseur , ProduitForm ,FrsForm ,UserRegistrationForm ,UserCreationForm
from django.urls import reverse
from django.db.models import Q 
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, authenticate
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from magasin.serializers import CategorySerializer , ProduitSerializer
from rest_framework import viewsets

# Create your views here.
@login_required
def home(request):
    context={'val':"Menu Acceuil"} 
    return render(request,'mesProduits.html',context)


def index(request):
    query = request.GET.get('q')
    if query:
        products = Produit.objects.filter(Q(libelle__icontains=query))
    else:
        products = Produit.objects.all()
    context = {'products': products, 'query': query}
    return render(request, 'magasin/mesProduits.html', context)


def register(request):
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password) 
            login(request,user)
            messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
            return redirect('home')
        else :
            form = UserCreationForm()
        return render(request,'registration/register.html',{'form' : form})


def IFournisseur(request):	
    template = loader.get_template('magasin/mesFournisseur.html')
    fournisseurs= Fournisseur.objects.all()
    context={'fournisseurs':fournisseurs}  
    return render( request,'magasin/mesProduits.html ',context )

def majProd(request):
    if request.method == "POST" : 
        form = ProduitForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/magasin')
    else :
        form = ProduitForm() #créer formulaire vide
        return render(request,'magasin/add_product.html',{'form':form})

def indexVtr(request):
    list=Produit.objects.all()
    return render(request,'../templates/magasin/vitrine.html',{'list':list})

def indexFrs(request): 
    if request.method == "POST" : 
        form = FrsForm(request.POST)
        if form.is_valid(): 
            nom = form.cleaned_data['nom']
            adr = form.cleaned_data['adr']
            frs=Fournisseur()
            frs.nom=nom
            frs.adresse=adr
            form.save()
    else :
        form = FrsForm()
    return render(request,'magasin/testForm.html',{'form':form})

"""
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('index')  # Change 'index' to the appropriate URL name.
            else:
                # Return an 'invalid login' error message.
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password.'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
"""
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = Produit.objects.get(id=product_id) 
        cart, _ = Cart.objects.get_or_create()
         
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return redirect('cart')

    return redirect('index')

def view_cart(request):
    cart, _ = Cart.objects.get_or_create()
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.subtotal() for item in cart_items)
    return render(request, 'magasin/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def decrease_quantity(request, product_id): 
    product = get_object_or_404(Produit, id=product_id)
     
    cart, _ = Cart.objects.get_or_create()
     
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
     
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
     
    return HttpResponseRedirect(reverse('cart'))

def remove_from_cart(request, product_id): 
    product = get_object_or_404(Produit, id=product_id)
     
    cart, _ = Cart.objects.get_or_create()
     
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
     
    return HttpResponseRedirect(reverse('cart'))

def generate_pdf(request):
    cart_items = CartItem.objects.all()   
     
    template_path = 'magasin/cart_pdf_template.html'
    context = {'cart_items': cart_items}
    template = get_template(template_path)
    html = template.render(context)
     
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cart_items.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF creation failed')
    return response
class CategoryAPIView(APIView):
 def get(self, *args, **kwargs):
    categories = Categorie.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
 
class ProductViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProduitSerializer
    def get_queryset(self):
        queryset = Produit.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categorie_id=category_id)
        return queryset
    
class ProduitAPIView(APIView):
    def get(self, *args, **kwargs):
        prods = Produit.objects.all()
        serializer = CategorySerializer(prods, many=True)
        return Response(serializer.data)