from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, ImageUploadForm
# from django.contrib.auth.models import User
from modules.users.models import User  # Modelo personalizado de usuarios
from django.contrib.auth import authenticate, login as iniciar, logout as salir
from django.http import HttpResponse
from .models import Images


def index(request):
    images = Images.objects.order_by("-timestamp")
    return render(request, 'landing/index.html', {'request': request, 'images': images})


def login(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                iniciar(request, user)  # Guarda en una cookie
                return redirect('landing:index')
            else:
                return HttpResponse("Usuario no encontrado motherfucker")

    return render(request,'landing/login.html', {"login":form})


def signup(request):
    form = SignupForm(request.POST or None)
    if request.method == 'POST':
        
        print(form.is_valid())
        if form.is_valid():
            form.cleaned_data.pop('confirm_password', None)
            user = User.objects.create_user(**form.cleaned_data)
            user.save()
            return redirect("landing:index")
    
    return render(request,'landing/sign.html',{'sign':form})


def logout(request):
    salir(request)
    return redirect("landing:index")


def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.save(commit=False)
            imagen.usuario = request.user
            imagen.save()
            return redirect("landing:index")
    else:
        form = ImageUploadForm()
        return render(request, 'landing/form_imagen.html', {'form': form})
