from django import forms
from django.db import models
from .models import Consulta, Receta, Medico, Paciente

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'fecha', 'duracion', 'sintomas', 'observaciones', 'diagnostico']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control'}),
            'sintomas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'medico': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super(ConsultaForm, self).__init__(*args, **kwargs)
        
        # Siempre mostrar todas las opciones disponibles
        self.fields['paciente'].queryset = Paciente.objects.all()
        self.fields['medico'].queryset = Medico.objects.all()
        
        # Personalizar campos basado en el usuario actual
        if usuario:
            if usuario.rol == 'medico':
                try:
                    medico = Medico.objects.get(usuario=usuario)
                    self.fields['medico'].initial = medico
                    self.fields['medico'].widget = forms.HiddenInput()
                except Medico.DoesNotExist:
                    pass
            elif usuario.rol == 'paciente':
                try:
                    paciente = Paciente.objects.get(usuario=usuario)
                    self.fields['paciente'].initial = paciente
                    self.fields['paciente'].widget = forms.HiddenInput()
                except Paciente.DoesNotExist:
                    pass

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['medicamentos', 'indicaciones']
        widgets = {
            'medicamentos': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'indicaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
