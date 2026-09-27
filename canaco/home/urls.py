from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('noticia/', views.noticia, name='noticia'), #[cite: 4]
    path('categoria/', views.categoria, name='categoria'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
]