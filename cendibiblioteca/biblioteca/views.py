from django.shortcuts import render
from .models import Libro, Prestamo

def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'biblioteca/lista_libros.html', {'libros': libros})

def lista_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'biblioteca/lista_prestamos.html', {'prestamos': prestamos})
