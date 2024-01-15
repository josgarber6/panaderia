from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import CustomerCreationForm, CustomerLoginForm, CustomPasswordChangeForm
from django.contrib import messages

def signup_view(request):
  if request.method == 'POST':
      form = CustomerCreationForm(request.POST)
      if form.is_valid():
          # save user to database
          form.save()
          # log user in
          username = form.cleaned_data.get('username')
          password = form.cleaned_data.get('password1')
          user = authenticate(request=request,username=username, password=password)
          login(request, user)
          return redirect('/')
  else:
      form = CustomerCreationForm()
  return render(request, 'authentication/signup.html', {'form': form})

def login_view(request):
  if request.method == 'POST':
      form = CustomerLoginForm(data=request.POST)
      if form.is_valid():
          # log user in
          username = form.cleaned_data.get('username')
          password = form.cleaned_data.get('password')
          user = authenticate(request=request,username=username, password=password)
          login(request, user)
          return redirect('/')
  else:
      form = CustomerLoginForm()
  return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
  logout(request)
  return redirect('/')

def change_password_view(request):
  if request.method == 'POST':
      form = CustomPasswordChangeForm(user=request.user, data=request.POST)
      if form.is_valid():
          # change password
          user = form.save()
          update_session_auth_hash(request, user)
          messages.success(request, 'Tu contraseña ha sido actualizada!')
          return redirect('/')
      else:
          messages.error(request, 'Por favor corrija el error.')
  else:
      form = CustomPasswordChangeForm(user=request.user)
  return render(request, 'authentication/change_password.html', {'form': form})