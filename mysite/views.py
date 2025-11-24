import os
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ClienteForm, SugerenciaForm
from collections import defaultdict

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

def ver_sugerencias(request):
    """Vista para que los clientes vean sus sugerencias"""
    cliente = Cliente.objects.get(user=request.user)
    sugerencias = cliente.sugerencia_set.all()
    
    return render(request, 'missugerencias.html', {
        'sugerencias': sugerencias,
    })

@login_required
def hacer_sugerencia(request):

    if request.method == 'POST':
        form = SugerenciaForm(request.POST)

        if form.is_valid():
            try:
                sugerencia = form.save(commit=False)

                # Obtener cliente
                cliente = Cliente.objects.get(user=request.user)

                sugerencia.cliente = cliente
                sugerencia.save()

                # Solo mensaje de éxito, sin correo
                return render(request, 'sugerencias.html', {
                    'form': SugerenciaForm(),
                    'mensaje_exito': True
                })

            except Cliente.DoesNotExist:
                return render(request, 'sugerencias.html', {
                    'form': form,
                    'error': 'No se encontró tu perfil de cliente. Contacta al administrador.'
                })
            except Exception as e:
                return render(request, 'sugerencias.html', {
                    'form': form,
                    'error': f'Error al procesar la sugerencia: {str(e)}'
                })
    else:
        form = SugerenciaForm()

    return render(request, 'sugerencias.html', {
        'form': form,
        'mensaje_exito': False
    })

@login_required
def todas_sugerencias(request):
    """Vista para que los administradores vean todas las sugerencias"""
    sugerencias = Sugerencia.objects.all().order_by('-fecha_creacion')
    
    return render(request, 'todas_sugerencias.html', {
        'sugerencias': sugerencias,
    })

def logout(request):
    auth_logout(request)
    return redirect('/')
def catalogo_view(request):

    if not request.user.is_authenticated:
        return redirect("index")

    # Intentar obtener cliente
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        cliente = None

    # Obtener categorías con sus productos
    categorias = Categoria.objects.prefetch_related("productos").all()

    # Procesar agregar al carrito
    if request.method == "POST":
        producto_id = request.POST.get("producto_id")
        cantidad = int(request.POST.get("cantidad", 1))

        producto = get_object_or_404(Producto, id=producto_id)

        # Obtener/crear carrito
        carrito, _ = Carrito.objects.get_or_create(
            cliente=cliente,
            pagado=False
        )

        carrito.agregar_producto(producto, cantidad)

        return redirect("catalogo")

    return render(request, "catalogo.html", {
        "categorias": categorias,
    })


@login_required
def carrito_view(request):
    # Obtener cliente
    cliente = get_object_or_404(Cliente, user=request.user)

    # Obtener o crear carrito activo
    carrito_activo, creado = Carrito.objects.get_or_create(
        cliente=cliente,
        pagado=False
    )

    # Items del carrito
    items = carrito_activo.items.all()

    # -----------------------------------
    # ELIMINAR PRODUCTO DEL CARRITO
    # -----------------------------------
    if request.method == "POST" and "eliminar_id" in request.POST:
        producto_id = request.POST.get("eliminar_id")
        producto = get_object_or_404(Producto, id=producto_id)

        carrito_activo.eliminar_producto(producto)

        return redirect("carrito")

    # -----------------------------------
    # PAGAR CARRITO
    # -----------------------------------
    if request.method == "POST" and "pagar" in request.POST:
        carrito_activo.pagar()
        return redirect("carrito")

    # Total del carrito
    total = carrito_activo.valor()

    return render(request, "carrito.html", {
        "carrito": carrito_activo,
        "items": items,
        "total": total,
    })
