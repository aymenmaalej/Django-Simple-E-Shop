from django.urls import path , include
from . import views
from .views import CategoryAPIView , ProduitAPIView

urlpatterns = [
    path('', views.index, name='index'),
    path('magasin/fournisseur', views.indexFrs, name='fournisseur'),
    path('magasin/vitrine', views.indexVtr, name='vitrine'),
    path('magasin/majprod', views.majProd, name='majprod'),
    path('magasin/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('magasin/cart/', views.view_cart, name='cart'),
    path('magasin/decrease_quantity/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('magasin/remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('magasin/generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('register/',views.register, name = 'register'),
    path('api/category/', CategoryAPIView.as_view()),
    path('api/produit/', ProduitAPIView.as_view()),
    path('api-auth/', include('rest_framework.urls'))

    
]
