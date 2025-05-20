from django import forms
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
        }
    
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super(ConsultaForm, self).__init__(*args, **kwargs)
        
        # Personalizar campos basado en el usuario actual
        if usuario and usuario.rol == 'medico':
            try:
                medico = Medico.objects.get(usuario=usuario)
                self.fields['medico'].initial = medico
                self.fields['medico'].widget = forms.HiddenInput()
                self.fields['paciente'].queryset = Paciente.objects.filter(medico_asignado=medico)
            except Medico.DoesNotExist:
                pass

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['medicamentos', 'indicaciones']
        widgets = {
            'medicamentos': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'indicaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
