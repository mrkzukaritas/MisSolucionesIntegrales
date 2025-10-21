
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('perfil/', views.perfil, name='perfil'),
    path('logout/', views.logout, name='logout'),
    path('admin-panel/', views.panel_administrador, name='panel_administrador'),
    path('sugerencias/', views.hacer_sugerencia, name='hacer_sugerencia'),
    path('perfil/sugerencias', views.ver_sugerencias, name='mis_sugerencias'),
    path('admin-panel/sugerencias', views.todas_sugerencias, name='todas_sugerencias'),
]