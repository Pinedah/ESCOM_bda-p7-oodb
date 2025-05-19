from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Usuario(AbstractUser):
    """Extensión de Django User para agregar campos específicos del sistema médico."""
    ROLES = (
        ('paciente', 'Paciente'),
        ('medico', 'Médico'),
        ('administrador', 'Administrador'),
    )
    
    # Eliminamos los campos username, first_name y last_name de AbstractUser
    # pero mantenemos username como opcional para compatibilidad con AbstractUser
    username = models.CharField(max_length=150, blank=True, null=True)
    first_name = None
    last_name = None
    
    # Agregamos campos según nuestra especificación
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField(null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    rol = models.CharField(max_length=15, choices=ROLES)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'rol']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_rol_display()})"


class Medico(models.Model):
    """Modelo para almacenar información específica de los médicos."""
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_medico')
    especialidad = models.CharField(max_length=255)
    numero_licencia = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"Dr. {self.usuario.nombre} - {self.especialidad}"
    
    def pacientes_asignados(self):
        """Retorna los pacientes asignados a este médico."""
        return self.pacientes.all()
    
    def consultas_pendientes(self):
        """Retorna las consultas pendientes del médico."""
        return self.consultas.filter(fecha__gt=timezone.now()).order_by('fecha')


class Paciente(models.Model):
    """Modelo para almacenar información específica de los pacientes."""
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_paciente')
    alergias = models.TextField(blank=True, null=True)
    enfermedades_previas = models.TextField(blank=True, null=True)
    tratamientos_actuales = models.TextField(blank=True, null=True)
    condiciones_heredadas = models.TextField(blank=True, null=True)
    contacto_emergencia = models.CharField(max_length=255, blank=True, null=True)
    medico_asignado = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, blank=True, related_name='pacientes')
    ultima_consulta = models.DateTimeField(blank=True, null=True)
    seguimiento = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.usuario.nombre}"
    
    def historial_consultas(self):
        """Retorna el historial de consultas del paciente."""
        return self.consultas.order_by('-fecha')
    
    def ultima_receta(self):
        """Retorna la última receta médica del paciente."""
        ultima_consulta = self.consultas.order_by('-fecha').first()
        if ultima_consulta and hasattr(ultima_consulta, 'receta'):
            return ultima_consulta.receta
        return None


class Consulta(models.Model):
    """Modelo para almacenar las consultas médicas."""
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='consultas')
    fecha = models.DateTimeField(default=timezone.now)
    duracion = models.IntegerField(help_text="Duración en minutos", null=True, blank=True)
    sintomas = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Consulta: {self.paciente} con Dr. {self.medico.usuario.nombre} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"
    
    def tiene_receta(self):
        """Verifica si la consulta tiene una receta asociada."""
        return hasattr(self, 'receta')
    
    def tiene_consentimiento(self):
        """Verifica si la consulta tiene un consentimiento asociado."""
        return self.consentimientos.exists()


class Receta(models.Model):
    """Modelo para almacenar recetas médicas."""
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE, related_name='receta')
    medicamentos = models.TextField()
    indicaciones = models.TextField()
    
    def __str__(self):
        return f"Receta para {self.consulta.paciente} - {self.consulta.fecha.strftime('%d/%m/%Y')}"


class Consentimiento(models.Model):
    """Modelo para almacenar consentimientos informados."""
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='consentimientos')
    documento = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Consentimiento: {self.consulta.paciente} - {self.fecha.strftime('%d/%m/%Y')}"


class TicketSoporte(models.Model):
    """Modelo para almacenar tickets de soporte técnico."""
    ESTADOS = (
        ('abierto', 'Abierto'),
        ('en proceso', 'En Proceso'),
        ('cerrado', 'Cerrado'),
    )
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tickets')
    asunto = models.CharField(max_length=255)
    descripcion = models.TextField()
    estado = models.CharField(max_length=15, choices=ESTADOS, default='abierto')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Ticket #{self.id}: {self.asunto} - {self.get_estado_display()}"
