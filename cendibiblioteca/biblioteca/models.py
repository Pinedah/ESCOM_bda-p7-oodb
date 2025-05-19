from django.db import models

# Create your models here.

class Alumno(models.Model):
    nombre_completo = models.CharField(max_length=100)
    escuela = models.CharField(max_length=50, default='CENDI IPN')
    ciclo_escolar = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre_completo

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Editorial(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    
    def __str__(self):
        return self.nombre

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=150)
    paginas = models.IntegerField()
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    autores = models.ManyToManyField(Autor)
    
    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.alumno} - {self.libro} - {self.fecha_prestamo}"
