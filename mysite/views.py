
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Cliente
from .forms import ClienteForm

def index(request):
    return render(request, 'index.html')

@login_required
def perfil(request):
    cliente = Cliente.objects.get(user=request.user)
    datos_completos = cliente.datos_completos()
    
    if request.method == 'POST' and 'editar' in request.POST:
        form = ClienteForm(instance=cliente)
        return render(request, 'perfil.html', {
            'cliente': cliente,
            'form': form,
            'datos_completos': False,
            'modo_edicion': True
        })
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'perfil.html', {
        'cliente': cliente,
        'form': form,
        'datos_completos': datos_completos,
        'modo_edicion': not datos_completos
    })

# VISTA SOLO PARA ADMINISTRADORES
def panel_administrador(request):
    """Panel exclusivo para administradores"""
    clientes = Cliente.objects.all()
    total_administradores = clientes.filter(rol='admin').count()
    total_clientes = clientes.filter(rol='cliente').count()
    
    return render(request, 'admin_panel.html', {
        'clientes': clientes,
        'total_usuarios': clientes.count(),
        'total_administradores': total_administradores,
        'total_clientes': total_clientes,
    })


def logout(request):
    auth_logout(request)
    return redirect('/')