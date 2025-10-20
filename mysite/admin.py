from django.contrib import admin
from .models import Producto
# Register your models here.
admin.site.site_header = "MIS Admin"
admin.site.register(Producto)