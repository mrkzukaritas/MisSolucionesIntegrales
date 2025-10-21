from django import forms
from .models import Cliente, Sugerencia

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cedula', 'direccion', 'telefono']
        widgets = {
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu cédula',
                'minlength': '6'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Ingresa tu dirección completa'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu teléfono'
            }),
        }
        labels = {
            'cedula': 'Cédula *',
            'direccion': 'Dirección *', 
            'telefono': 'Teléfono *',
        }
        error_messages = {
            'cedula': {
                'required': 'La cédula es obligatoria',
                'min_length': 'La cédula debe tener al menos 6 caracteres',
            },
            'direccion': {
                'required': 'La dirección es obligatoria',
            },
            'telefono': {
                'required': 'El teléfono es obligatorio',
            },
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if cedula:
            # Validar que tenga al menos 6 caracteres
            if len(cedula) < 6:
                raise forms.ValidationError('La cédula debe tener al menos 6 caracteres')
            # Validar que solo contenga números y guiones
            if not all(c.isdigit() or c == '-' for c in cedula):
                raise forms.ValidationError('La cédula solo puede contener números y guiones')
        return cedula

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Validar que solo contenga números, espacios, paréntesis y +
            if not all(c.isdigit() or c in ' +-()' for c in telefono):
                raise forms.ValidationError('El teléfono solo puede contener números y los caracteres: + - ( )')
        return telefono

    def clean(self):
        cleaned_data = super().clean()
        cedula = cleaned_data.get('cedula')
        direccion = cleaned_data.get('direccion')
        telefono = cleaned_data.get('telefono')

        # Validar que todos los campos estén completos
        if not cedula:
            self.add_error('cedula', 'Este campo es obligatorio')
        if not direccion:
            self.add_error('direccion', 'Este campo es obligatorio')
        if not telefono:
            self.add_error('telefono', 'Este campo es obligatorio')

        return cleaned_data
    
class SugerenciaForm(forms.ModelForm):
    class Meta:
        model = Sugerencia
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Escribe tu sugerencia aquí...'
            }),
        }
        labels = {
            'contenido': 'Sugerencia *',
        }
        error_messages = {
            'contenido': {
                'required': 'El contenido de la sugerencia es obligatorio',
            },
        }