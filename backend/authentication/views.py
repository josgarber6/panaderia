from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from .forms import CustomerCreationForm, CustomerLoginForm
from django.views.generic import FormView, TemplateView
from django_otp.decorators import otp_required
from django.conf import settings

def signup_view(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            # Save user to database
            form.save()
        return redirect('signup_complete')
    else:
        form = CustomerCreationForm()
    return render(request, 'authentication/signup.html', {'form': form})

class SignupCompleteView(TemplateView):
    template_name = 'authentication/signup_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context
    
def signup_complete_view(request, *args, **kwargs):
    context = {}
    context['login_url'] = resolve_url(settings.LOGIN_URL)
    return render(request, 'authentication/signup_complete.html', context)
    
def logout_view(request):
  logout(request)
  return redirect('/')

@otp_required
def change_password_view(request):
  if request.method == 'POST':
      form = PasswordChangeForm(data=request.POST)
      if form.is_valid():
          # change password
          form.save()
          return redirect('/')
  else:
      form = PasswordChangeForm(user=request.user)
  return render(request, 'authentication/change_password.html', {'form': form})