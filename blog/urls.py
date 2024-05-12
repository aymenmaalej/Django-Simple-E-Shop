from django.urls import path,include
from django.contrib import admin
from .views import *
urlpatterns = [
    path('', Post_listView.as_view(), name='post-list'),
    path('<int:pk>/detailPost',DetailPost.as_view(), name='detailPost'),
    path('addPost/', CreerPost.as_view(), name='addPost'),
    path('<int:pk>/modifier/', ModifierPost.as_view(), name='editPost'),
    path('<int:pk>/supprimer/', SupprimerPost.as_view(), name='deletePost'),

]