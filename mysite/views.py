import json
from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from decouple import config
from django.shortcuts import redirect
from .models import Cliente
from .forms import ClienteForm
from urllib.parse import urlencode
from social_django.models import UserSocialAuth
# Create your views here.
def index(request):
    return render(request, 'index.html')

def perfil(request):
    cliente, created = Cliente.objects.get_or_create(user=request.user)

    # Si todos los datos ya existen y no viene un POST, mostrar solo la info
    datos_completos = all([
        cliente.cedula,
        cliente.direccion,
        cliente.telefono
    ])
    if request.method == 'POST' and 'editar' in request.POST:
        return render(request, 'perfil.html', {
            'cliente': cliente,
            'form': ClienteForm(instance=cliente),
            'datos_completos': False,  # muestra el formulario
        })
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # recarga la página en modo "solo lectura"
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'perfil.html', {
        'cliente': cliente,
        'form': form,
        'datos_completos': datos_completos,
    })

def logout(request):
    auth_logout(request)
    domain = config('APP_DOMAIN')
    client_id = config('APP_CLIENT_ID')
    return_to = request.build_absolute_uri('/')  # genera http://localhost:8000/
    params = urlencode({
        'client_id': client_id,
        'returnTo': return_to,
    })
    logout_url = f"https://{domain}/v2/logout?{params}"
    return redirect(logout_url)

