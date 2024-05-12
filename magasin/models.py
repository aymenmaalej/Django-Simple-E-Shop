from datetime import date
from django.db import models

class Categorie(models.Model):
    TYPE_CHOICES = [
        ('Al','Alimentaire'),
        ('Mb','Meuble'),
        ('Sn','Sanitaire'),
        ('Vs','Vaisselle'),
        ('Vt','Vetement'),
        ('Jx','Jouets'),
        ('Lg','Linge de Maison'),
        ('Bj','Bijoux'),
        ('Dc','Décor')
    ]
    name = models.CharField(max_length=50, default='Alimentaire', choices=TYPE_CHOICES)
    
    def __str__(self):
        return f"{self.name}"

class Produit(models.Model):
    libelle = models.CharField(max_length=100)
    description = models.TextField(default="")
    prix = models.DecimalField(max_digits=10, decimal_places=3)
    TYPE_CHOICES = [
        ('em','emballé'),
        ('fr','Frais'),
        ('cs','Conserve')
    ]
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='em')
    Img = models.ImageField(blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.libelle} - {self.description} - {self.prix} - {self.type}"

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    email = models.EmailField()
    telephone = models.CharField(max_length=8)

    def __str__(self):
        return self.nom

class Commande(models.Model):
    dateCde = models.DateField(null=True, default=date.today)
    totalCde = models.DecimalField(max_digits=10, decimal_places=3)
    produits = models.ManyToManyField(Produit) 
    
    def __str__(self):
        return f"{self.dateCde} - {self.totalCde}"

class ProduitNC(Produit):
    duree_garantie = models.CharField(max_length=100)
    def __str__(self):
        return super().__str__()+" "+self.duree_garantie
        
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.prix * self.quantity
