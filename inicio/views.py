from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
def home(request):
    return render(request, 'inicio.html',{
        'form': UserCreationForm()
    }
    )
