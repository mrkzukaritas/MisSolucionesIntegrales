# Register your models here.
from django.contrib import admin
from .models import Categoria, Producto, carrito, ItemCarrito, Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'email', 'cedula', 'telefono', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'cedula']
    
    def nombre_completo(self, obj):
        return obj.user.get_full_name()
    nombre_completo.short_description = 'Nombre'
    
    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'
# ---------------------------
#   CATEGORIA
# ---------------------------
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
# ---------------------------
#   PRODUCTO
# ---------------------------
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "codigo", "precio", "stock", "categoria")
    search_fields = ("nombre", "codigo")
    list_filter = ("categoria",)
    list_editable = ("precio", "stock")  # Para editar desde la tabla
    ordering = ("nombre",)


# ---------------------------
#   ITEM CARRITO (solo lectura desde inline)
# ---------------------------
class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0
    readonly_fields = ("producto", "cantidad")


# ---------------------------
#   CARRITO
# ---------------------------
@admin.register(carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "pagado")
    list_filter = ("pagado",)
    search_fields = ("cliente__user__username", "cliente__user__first_name", "cliente__user__last_name")
    inlines = [ItemCarritoInline]
