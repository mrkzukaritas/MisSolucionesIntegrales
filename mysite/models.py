from django.db import models
from django.contrib.auth.models import User #usuario autenticado

# Create your models here.

#las catergorias de los productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    #imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')

    def vender(self, cantidad):
        if cantidad > self.stock:
            raise ValueError("No hay suficiente stock disponible.")
        self.stock -= cantidad
        self.save()

    def comprar(self, cantidad):
        self.stock += cantidad
        self.save()

    def __str__(self):
        return f"{self.nombre} ({self.categoria})" if self.categoria else self.nombre


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=15, unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.cedula}"