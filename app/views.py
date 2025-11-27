from django.shortcuts import render
from .models import Producto

def index(request):
    # Traemos todos los productos de la base de datos
    productos = Producto.objects.all()  
    return render(request, 'app/index.html', {'productos': productos})