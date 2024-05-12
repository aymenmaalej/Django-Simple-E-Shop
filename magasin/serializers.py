from rest_framework.serializers import ModelSerializer 

from .models import Categorie , Produit

class CategorySerializer(ModelSerializer):
 class Meta:
    models = Categorie
    fields = ['id', 'name']

class ProduitSerializer(ModelSerializer):
 class Meta:
    models = Produit
    fields = ['id', 'libelle','description']
