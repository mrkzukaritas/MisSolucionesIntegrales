import json
from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from decouple import config
from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import urlencode
# Create your views here.
def index(request):
    return render(request, 'index.html')

def perfil(request):
    user = request.user

    auth0_user =  user.social_auth.get(provider='auth0')
    user_info = {
        'user_id': auth0_user.uid,
        'name': auth0_user.extra_data.get('name', user.get_full_name() or user.username),
        'picture': auth0_user.extra_data.get('picture'),
        'email': auth0_user.extra_data.get('email', user.email),
    }

    contex={'user_infor': json.dumps(user_info, indent=4),
            'auth0_user':auth0_user
            }
    return render(request, 'perfil.html',contex)

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

