import os
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ClienteForm, SugerenciaForm
from django.core.mail import send_mail

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

def enviar_email_con_reintentos(asunto, mensaje, email_destino, max_reintentos=3):
    """Envía email con reintentos automáticos si falla"""
    print(f"🚀 INICIANDO ENVÍO DE EMAIL a: {email_destino}")
    
    for intento in range(max_reintentos):
        try:
            print(f"📧 Intento {intento + 1} de {max_reintentos}...")
            
            # VERIFICAR CONFIGURACIÓN ANTES DE ENVIAR
            email_user = os.environ.get('EMAIL_HOST_USER')
            print(f"🔧 Configuración - EMAIL_HOST_USER: {email_user}")
            
            if not email_user:
                print("❌ ERROR: EMAIL_HOST_USER no está configurado")
                return False
                
            resultado = send_mail(
                asunto,
                mensaje,
                email_user,  # Usar el mismo email como remitente
                [email_destino],
                fail_silently=False,

            )
            
            print(f"✅ Email enviado EXITOSAMENTE. Resultado: {resultado}")
            return True
            
        except Exception as e:
            if intento < max_reintentos - 1:
                time.sleep(2)
            continue

    return False

@login_required
def hacer_sugerencia(request):

    if request.method == 'POST':

        form = SugerenciaForm(request.POST)

        if form.is_valid():
            try:
                sugerencia = form.save(commit=False)

                # VERIFICAR SI EL CLIENTE EXISTE
                cliente = Cliente.objects.get(user=request.user)

                sugerencia.cliente = cliente
                sugerencia.save()

                asunto = '✅ Sugerencia recibida - Mis Soluciones Integrales'
                mensaje = f'''Hola {cliente.user.first_name},

Gracias por enviar tu sugerencia. Hemos recibido el siguiente contenido:

"{sugerencia.contenido}"

La revisaremos pronto y te mantendremos informado sobre su estado.

📅 Fecha: {sugerencia.fecha_creacion.strftime("%d/%m/%Y %H:%M")}

Saludos,
Equipo de Mis Soluciones Integrales'''

                # Enviar correo de confirmación CON REINTENTOS
                email_enviado = enviar_email_con_reintentos(
                    asunto, 
                    mensaje, 
                    cliente.user.email
                )

                # Mensaje de éxito
                return render(request, 'sugerencias.html', {
                    'form': SugerenciaForm(),
                    'mensaje_exito': True,
                    'email_enviado': email_enviado
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

def todas_sugerencias(request):
    """Vista para que los administradores vean todas las sugerencias"""
    sugerencias = Sugerencia.objects.all().order_by('-fecha_creacion')
    
    return render(request, 'todas_sugerencias.html', {
        'sugerencias': sugerencias,
    })

def logout(request):
    auth_logout(request)
    return redirect('/')


@login_required
def catalogo_view(request):
    # Validar que haya usuario autenticado
    if not request.user.is_authenticated:
        return redirect("login")

    # Obtener el cliente — si no existe, evita error
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        cliente = None  # evita que se caiga la vista

    categorias = Categoria.objects.all()
    productos = Producto.objects.all()

    return render(request, "catalogo.html", {
        "cliente": cliente,
        "categorias": categorias,
        "productos": productos,
    })
@login_required
def carrito_view(request):
    cliente = Cliente.objects.get(user=request.user)

    carrito_activo = carrito.objects.get(cliente=cliente, pagado=False)

    items = carrito_activo.items.all()

    # ELIMINAR PRODUCTO
    if request.method == "POST" and "eliminar_id" in request.POST:
        producto_id = request.POST.get("eliminar_id")
        producto = get_object_or_404(Producto, id=producto_id)

        carrito_activo.eliminar_producto(producto)

        return redirect("carrito")

    # PAGAR
    if request.method == "POST" and "pagar" in request.POST:
        carrito_activo.pagar()
        return redirect("carrito")  # esto ya muestra el carrito nuevo vacío

    # CALCULAR TOTAL
    total = carrito_activo.valor()

    return render(request, "carrito.html", {
        "carrito": carrito_activo,
        "items": items,
        "total": total,
    })
