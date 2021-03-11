from django.urls import path
from . import views

urlpatterns = [
    path('', views.movieforselect, name='index'),

    path('movieforselect/', views.movieforselect),
    path('castforselect/', views.castforselect),
    path('armake/', views.armake),
    path('movieinfo/', views.movieinfo),
]
