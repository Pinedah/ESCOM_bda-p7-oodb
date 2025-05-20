from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from medical.models import Medico, Paciente
import getpass

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Crea un superusuario con opción de asignarle perfil de médico o paciente'

    def handle(self, *args, **kwargs):
        email = input("Email: ")
        nombre = input("Nombre: ")
        
        # Validar email único
        if Usuario.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f"El email {email} ya está en uso"))
            return
        
        # Pedir y confirmar contraseña
        password = getpass.getpass("Contraseña: ")
        password_confirm = getpass.getpass("Confirmación de contraseña: ")
        
        if password != password_confirm:
            self.stdout.write(self.style.ERROR("Las contraseñas no coinciden"))
            return
        
        # Crear el superusuario
        user = Usuario.objects.create_superuser(
            email=email,
            nombre=nombre,
            password=password,
            rol='administrador'
        )
        
        self.stdout.write(self.style.SUCCESS(f"Superusuario {email} creado exitosamente"))
        
        # Preguntar si quiere añadir perfil médico o paciente
        self.stdout.write("\n¿Desea añadir un perfil adicional a este usuario?")
        self.stdout.write("1) Añadir perfil de médico")
        self.stdout.write("2) Añadir perfil de paciente")
        self.stdout.write("3) No añadir perfil adicional")
        
        option = input("Seleccione una opción (1-3): ")
        
        if option == '1':
            especialidad = input("Especialidad médica: ")
            numero_licencia = input("Número de licencia: ")
            
            medico = Medico.objects.create(
                usuario=user,
                especialidad=especialidad,
                numero_licencia=numero_licencia
            )
            user.rol = 'medico'
            user.save()
            
            self.stdout.write(self.style.SUCCESS(f"Perfil de médico creado para {email}"))
        
        elif option == '2':
            Paciente.objects.create(
                usuario=user,
                alergias="Ninguna registrada",
                enfermedades_previas="Ninguna registrada"
            )
            user.rol = 'paciente'
            user.save()
            
            self.stdout.write(self.style.SUCCESS(f"Perfil de paciente creado para {email}"))
