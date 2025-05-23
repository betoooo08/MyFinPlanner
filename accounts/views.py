from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html', {
        'active_page': 'home'
    })

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente
            messages.success(request, 'Your account has been created successfully!')
            return redirect('dashboard')
        else:
            print(form.errors)  # Esto imprimirá los errores en la consola
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    return render(request, 'login.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html', {
        'user': request.user
    })