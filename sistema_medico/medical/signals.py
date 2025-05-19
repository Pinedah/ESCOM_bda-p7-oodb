from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='medical.Usuario')
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crea automáticamente el perfil correspondiente al crear un usuario."""
    # Import models inside the function to avoid circular import
    from medical.models import Medico, Paciente
    
    if created:
        if instance.rol == 'medico':
            Medico.objects.create(usuario=instance)
        elif instance.rol == 'paciente':
            Paciente.objects.create(usuario=instance)


@receiver(post_save, sender='medical.Consulta')
def actualizar_ultima_consulta(sender, instance, **kwargs):
    """Actualiza la fecha de última consulta del paciente."""
    paciente = instance.paciente
    if not paciente.ultima_consulta or instance.fecha > paciente.ultima_consulta:
        paciente.ultima_consulta = instance.fecha
        paciente.save(update_fields=['ultima_consulta'])
