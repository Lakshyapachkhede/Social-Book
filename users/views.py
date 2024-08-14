from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import logout, login
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            login(request.user)
            return redirect('post-home')
        
    else:
        form = forms.UserRegisterForm()

    return render(request, 'users/register.html', {'form':form})
            
@login_required
@require_GET
def logout_view(request):
    logout(request)

    return render(request, 'users/logout.html')