from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from medical.models import Medico, Paciente

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Crea usuarios de prueba: 1 médico y 2 pacientes'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creando usuarios de prueba...')
        
        # Crear un médico
        if not Usuario.objects.filter(email='medico@example.com').exists():
            medico_user = Usuario.objects.create_user(
                email='medico@example.com',
                nombre='Dr. Juan Pérez',
                password='medico123',
                rol='medico'
            )
            
            Medico.objects.create(
                usuario=medico_user,
                especialidad='Medicina General',
                numero_licencia='MED-12345'
            )
            
            self.stdout.write(self.style.SUCCESS('Médico creado: medico@example.com (password: medico123)'))
        else:
            self.stdout.write('El médico ya existe, saltando creación.')
        
        # Crear pacientes
        for i in range(1, 3):
            email = f'paciente{i}@example.com'
            
            # Verificar si el usuario ya existe
            usuario_existente = Usuario.objects.filter(email=email).first()
            
            if not usuario_existente:
                # Crear nuevo usuario y perfil de paciente
                paciente_user = Usuario.objects.create_user(
                    email=email,
                    nombre=f'Paciente {i}',
                    password='paciente123',
                    rol='paciente'
                )
                
                Paciente.objects.create(
                    usuario=paciente_user,
                    alergias='Ninguna conocida',
                    enfermedades_previas='Ninguna reportada'
                )
                
                self.stdout.write(self.style.SUCCESS(f'Paciente creado: {email} (password: paciente123)'))
            else:
                # Verificar si ya tiene un perfil de paciente
                if not hasattr(usuario_existente, 'perfil_paciente'):
                    # Si el usuario existe pero no tiene perfil de paciente, crear el perfil
                    Paciente.objects.create(
                        usuario=usuario_existente,
                        alergias='Ninguna conocida',
                        enfermedades_previas='Ninguna reportada'
                    )
                    self.stdout.write(self.style.SUCCESS(f'Perfil de paciente creado para usuario existente: {email}'))
                else:
                    self.stdout.write(f'El paciente {email} ya existe, saltando creación.')
        
        self.stdout.write(self.style.SUCCESS('Usuarios de prueba creados exitosamente'))
