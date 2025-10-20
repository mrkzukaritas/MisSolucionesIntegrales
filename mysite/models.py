from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class Cliente(models.Model):
    # Roles disponibles - SOLO ADMIN Y CLIENTE
    ROLES = (
        ('cliente', 'Cliente Normal'),
        ('admin', 'Administrador'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    cedula = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name="Cédula",
        validators=[MinLengthValidator(6)]
    )
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente', verbose_name="Rol")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.email}"

    def datos_completos(self):
        return all([self.cedula, self.direccion, self.telefono])
    
    def es_administrador(self):
        return self.rol == 'admin'
    
    def es_cliente_normal(self):
        return self.rol == 'cliente'