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
    

class Sugerencia(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    contenido = models.TextField(verbose_name="Contenido de la Sugerencia")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sugerencia"
        verbose_name_plural = "Sugerencias"

    def __str__(self):
        return f"Sugerencia de {self.cliente.user.get_full_name()} - {self.fecha_creacion.strftime('%Y-%m-%d %H:%M')}"
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="productos")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
class ItemCarrito(models.Model):
    
    carrito = models.ForeignKey('carrito', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
class carrito(models.Model):

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    #lista de productos en el carrito
    productos= models.ManyToManyField(ItemCarrito, through=ItemCarrito)
    pagado= models.BooleanField(default=False)

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"
        unique_together = ('cliente', 'producto')
    def pagar(self):
        if self.pagado!= True:
            self.pagado = True
            self.productos.clear()

        self.save()
    def agregar_producto(self, producto, cantidad):

        item, created = ItemCarrito.objects.get_or_create(carrito=self, producto=producto)
        if not created:
            item.cantidad += cantidad
        else:
            item.cantidad = cantidad
        item.save()
    def buscar_producto(self, producto):
        try:
            return ItemCarrito.objects.get(carrito=self, producto=producto)
        except ItemCarrito.DoesNotExist:    
            return None
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} para {self.cliente.user.get_full_name()}"