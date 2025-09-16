from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm


def singup(request):
    if request.method =='GET':
        print("llego")
    else:
        print("se registro un usuario")
        print(request.POST)
    return render(request, 'singup.html',{
        'form': UserCreationForm()
    }
    )

def home(request):
    return render(request, 'home.html')