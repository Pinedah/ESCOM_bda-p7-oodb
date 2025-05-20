from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Consulta, Paciente, Medico, Receta
from .forms import ConsultaForm, RecetaForm, LoginForm

def index(request):
    """Vista para la página principal."""
    return render(request, 'medical/index.html')

def login_view(request):
    """Vista para iniciar sesión."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Credenciales inválidas')
    else:
        form = LoginForm()
    
    return render(request, 'medical/login.html', {'form': form})

def logout_view(request):
    """Vista para cerrar sesión."""
    logout(request)
    return redirect('login')

@login_required
def consulta_list(request):
    """Vista para listar consultas."""
    # Filtrar consultas según el rol del usuario
    if request.user.rol == 'medico':
        try:
            medico = Medico.objects.get(usuario=request.user)
            consultas = Consulta.objects.filter(medico=medico).order_by('-fecha')
        except Medico.DoesNotExist:
            consultas = []
    elif request.user.rol == 'paciente':
        try:
            paciente = Paciente.objects.get(usuario=request.user)
            consultas = Consulta.objects.filter(paciente=paciente).order_by('-fecha')
        except Paciente.DoesNotExist:
            consultas = []
    elif request.user.rol == 'administrador' or request.user.is_staff:
        consultas = Consulta.objects.all().order_by('-fecha')
    else:
        consultas = []
    
    return render(request, 'medical/consulta_list.html', {'consultas': consultas})

@login_required
def consulta_detail(request, pk):
    """Vista para ver detalles de una consulta."""
    consulta = get_object_or_404(Consulta, pk=pk)
    # Verificar si el usuario tiene permiso para ver esta consulta
    if request.user.rol == 'paciente' and consulta.paciente.usuario != request.user:
        messages.error(request, 'No tienes permiso para ver esta consulta.')
        return redirect('consulta_list')
    elif request.user.rol == 'medico' and consulta.medico.usuario != request.user:
        messages.error(request, 'No tienes permiso para ver esta consulta.')
        return redirect('consulta_list')
    
    try:
        receta = consulta.receta
    except Receta.DoesNotExist:
        receta = None
    
    return render(request, 'medical/consulta_detail.html', {'consulta': consulta, 'receta': receta})

@login_required
def consulta_new(request):
    """Vista para crear una nueva consulta."""
    # Solo médicos y administradores pueden crear consultas
    if request.user.rol not in ['medico', 'administrador'] and not request.user.is_staff:
        messages.error(request, 'No tienes permisos para crear consultas.')
        return redirect('consulta_list')
    
    if request.method == "POST":
        form = ConsultaForm(request.POST, usuario=request.user)
        if form.is_valid():
            consulta = form.save()
            messages.success(request, 'Consulta creada exitosamente.')
            return redirect('consulta_detail', pk=consulta.pk)
    else:
        form = ConsultaForm(usuario=request.user)
    
    return render(request, 'medical/consulta_form.html', {'form': form})

@login_required
def consulta_edit(request, pk):
    """Vista para editar una consulta existente."""
    consulta = get_object_or_404(Consulta, pk=pk)
    
    # Verificar permisos
    if request.user.rol == 'medico' and consulta.medico.usuario != request.user:
        messages.error(request, 'No tienes permiso para editar esta consulta.')
        return redirect('consulta_list')
    elif request.user.rol == 'paciente':
        messages.error(request, 'No tienes permiso para editar consultas.')
        return redirect('consulta_list')
    
    if request.method == "POST":
        form = ConsultaForm(request.POST, instance=consulta, usuario=request.user)
        if form.is_valid():
            consulta = form.save()
            messages.success(request, 'Consulta actualizada exitosamente.')
            return redirect('consulta_detail', pk=consulta.pk)
    else:
        form = ConsultaForm(instance=consulta, usuario=request.user)
    
    return render(request, 'medical/consulta_form.html', {'form': form})

@login_required
def consulta_delete(request, pk):
    """Vista para eliminar una consulta."""
    consulta = get_object_or_404(Consulta, pk=pk)
    
    # Verificar permisos
    if request.user.rol != 'administrador' and not request.user.is_staff:
        messages.error(request, 'Solo los administradores pueden eliminar consultas.')
        return redirect('consulta_list')
    
    if request.method == "POST":
        consulta.delete()
        messages.success(request, 'Consulta eliminada exitosamente.')
        return redirect('consulta_list')
    
    return render(request, 'medical/consulta_confirm_delete.html', {'consulta': consulta})

@login_required
def receta_add(request, consulta_id):
    """Vista para añadir una receta a una consulta."""
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    
    # Verificar permisos
    if request.user.rol != 'medico' or (request.user.rol == 'medico' and consulta.medico.usuario != request.user):
        messages.error(request, 'No tienes permiso para añadir recetas.')
        return redirect('consulta_detail', pk=consulta_id)
    
    if hasattr(consulta, 'receta'):
        messages.error(request, 'Esta consulta ya tiene una receta asociada.')
        return redirect('consulta_detail', pk=consulta_id)
    
    if request.method == "POST":
        form = RecetaForm(request.POST)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.consulta = consulta
            receta.save()
            messages.success(request, 'Receta añadida exitosamente.')
            return redirect('consulta_detail', pk=consulta_id)
    else:
        form = RecetaForm()
    
    return render(request, 'medical/receta_form.html', {'form': form, 'consulta': consulta})
