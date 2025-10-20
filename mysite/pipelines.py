# mysite/pipelines.py
from .models import Cliente

def save_profile(backend, user, response, *args, **kwargs):
    if not hasattr(user, 'cliente'):
        cedula = response.get('nickname', '') or f"tmp-{user.id}"
        Cliente.objects.create(
            user=user,
            cedula=cedula,
        )
