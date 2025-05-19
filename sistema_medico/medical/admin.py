from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, 
    Medico, 
    Paciente, 
    Consulta, 
    Receta, 
    Consentimiento, 
    TicketSoporte
)

class MedicoInline(admin.StackedInline):
    model = Medico
    can_delete = False
    verbose_name_plural = 'Perfil Médico'

class PacienteInline(admin.StackedInline):
    model = Paciente
    can_delete = False
    verbose_name_plural = 'Perfil Paciente'

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('nombre', 'email', 'rol', 'is_active')
    list_filter = ('rol', 'is_active')
    search_fields = ('nombre', 'email')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('nombre', 'fecha_nacimiento', 'telefono', 'rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'fecha_nacimiento', 'rol', 'password1', 'password2'),
        }),
    )
    
    def get_inlines(self, request, obj=None):
        if obj:
            if obj.rol == 'medico':
                return [MedicoInline]
            elif obj.rol == 'paciente':
                return [PacienteInline]
        return []

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'especialidad', 'numero_licencia')
    search_fields = ('usuario__nombre', 'especialidad', 'numero_licencia')
    list_filter = ('especialidad',)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'medico_asignado', 'ultima_consulta')
    search_fields = ('usuario__nombre', 'medico_asignado__usuario__nombre')
    list_filter = ('medico_asignado',)

class RecetaInline(admin.TabularInline):
    model = Receta
    can_delete = True
    extra = 1

class ConsentimientoInline(admin.TabularInline):
    model = Consentimiento
    can_delete = True
    extra = 1

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'fecha', 'diagnostico', 'tiene_receta')
    list_filter = ('fecha', 'medico')
    search_fields = ('paciente__usuario__nombre', 'medico__usuario__nombre', 'diagnostico')
    date_hierarchy = 'fecha'
    inlines = [RecetaInline, ConsentimientoInline]

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('consulta', 'medicamentos_resumen')
    search_fields = ('consulta__paciente__usuario__nombre', 'medicamentos')
    
    def medicamentos_resumen(self, obj):
        return obj.medicamentos[:50] + '...' if len(obj.medicamentos) > 50 else obj.medicamentos
    medicamentos_resumen.short_description = 'Medicamentos'

@admin.register(Consentimiento)
class ConsentimientoAdmin(admin.ModelAdmin):
    list_display = ('consulta', 'fecha')
    search_fields = ('consulta__paciente__usuario__nombre',)
    date_hierarchy = 'fecha'

@admin.register(TicketSoporte)
class TicketSoporteAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'asunto', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('usuario__nombre', 'asunto', 'descripcion')
    date_hierarchy = 'fecha_creacion'
