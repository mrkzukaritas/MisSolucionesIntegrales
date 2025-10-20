import os
from .models import Cliente

def save_profile(backend, user, response, *args, **kwargs):
    """
    Pipeline para crear/actualizar el perfil y asignar roles por email
    """
    if backend.name == 'google-oauth2':
        email = user.email.lower()
        
        try:
            # Obtener emails de administradores desde .env
            admin_emails_str = os.environ.get('ADMIN_EMAILS', '')
            
            # Convertir string a lista y limpiar espacios
            emails_administradores = [
                email.strip().lower() 
                for email in admin_emails_str.split(',') 
                if email.strip()
            ]
            
            # Si no hay emails configurados, usar una lista vacía
            if not emails_administradores:
                emails_administradores = []
                print("⚠️ No hay emails de administradores configurados en .env")
            
        except Exception as e:
            print(f"❌ Error leyendo ADMIN_EMAILS: {e}")
            emails_administradores = []
    
        
        # Determinar el rol según el email
        if email in emails_administradores:
            rol = 'admin'
            print(f"🎯 ADMINISTRADOR DETECTADO: {email}")
        else:
            rol = 'cliente'
            print(f"👍 CLIENTE NORMAL: {email}")
        
        # Crear o actualizar el cliente
        cliente, created = Cliente.objects.get_or_create(user=user)
        cliente.rol = rol
        cliente.save()
        
        # Actualizar información del usuario
        if response.get('email'):
            user.email = response.get('email')
        
        if response.get('given_name'):
            user.first_name = response.get('given_name')
        
        if response.get('family_name'):
            user.last_name = response.get('family_name')
        
        user.save()
        
        print(f"✅ ROL ASIGNADO: {rol} para {user.email}")