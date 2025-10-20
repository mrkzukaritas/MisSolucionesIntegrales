# Register your models here.

from django.contrib import admin
from .models import Cliente

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