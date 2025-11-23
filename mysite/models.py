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
    carrito = models.ForeignKey('carrito', on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
class Carrito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    pagado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def __str__(self):
        return f"Carrito #{self.id} - {self.cliente.user.get_full_name()} - Pagado: {self.pagado}"

    # -----------------------------
    # PAGAR CARRITO
    # -----------------------------
    def pagar(self):
        if not self.pagado:
            self.pagado = True
            self.save()

            # Crear un nuevo carrito vacío para seguir comprando
            Carrito.objects.create(cliente=self.cliente)

    # -----------------------------
    # AGREGAR PRODUCTO
    # -----------------------------
    def agregar_producto(self, producto, cantidad):
        # 1. Validar stock
        if producto.stock < cantidad:
            return False  # No hay stock

        # 2. Crear SIEMPRE un ItemCarrito nuevo
        item = ItemCarrito.objects.create(
            carrito=self,
            producto=producto,
            cantidad=cantidad
        )

        # 3. Descontar del stock
        producto.stock -= cantidad
        producto.save()

        return True
    # -----------------------------
    # ELIMINAR PRODUCTO
    # -----------------------------
    def eliminar_producto(self, producto):
        """
        Elimina un producto del carrito.
        - Si existe el ItemCarrito, se borra.
        - Se devuelve la cantidad al stock del producto.
        """
        try:
            item = ItemCarrito.objects.get(carrito=self, producto=producto)
        except ItemCarrito.DoesNotExist:
            return False  # No existía en el carrito

        # Devolver al stock
        producto.stock += item.cantidad
        producto.save()

        # Eliminar item del carrito
        item.delete()

        return True
    # -----------------------------
    # BUSCAR PRODUCTO EN EL CARRITO
    # -----------------------------
    def buscar_producto(self, producto):
        try:
            return ItemCarrito.objects.filter(carrito=self, producto=producto)
        except ItemCarrito.DoesNotExist:
            return None
    
    def valor(self):
        """
        Retorna la suma total de todos los items del carrito:
        precio * cantidad
        """
        total = 0
        for item in self.items.all():
            total += item.producto.precio * item.cantidad
        return total