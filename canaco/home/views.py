from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html')

def noticia(request):
    return render(request, 'home/noticia.html')

def categoria(request):
    return render(request, 'home/categoria.html')

def login_view(request):
    return render(request, 'home/login.html')

def registro(request):
    return render(request, 'home/registro.html')