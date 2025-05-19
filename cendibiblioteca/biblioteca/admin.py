from django.contrib import admin
from .models import Alumno, Especialidad, Editorial, Autor, Libro, Prestamo

admin.site.register(Alumno)
admin.site.register(Especialidad)
admin.site.register(Editorial)
admin.site.register(Autor)
admin.site.register(Libro)
admin.site.register(Prestamo)
