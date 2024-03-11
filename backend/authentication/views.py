from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from .forms import CustomerCreationForm, CustomerLoginForm
from django.views.generic import FormView, TemplateView
from django_otp.decorators import otp_required
from django.conf import settings
# Session cookies
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.http import JsonResponse

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
    
def logout_view(request):
  logout(request)
  return redirect('http://localhost:5173/')


def get_username_from_session(request):
    session_id = request.COOKIES['sessionid']
    try:
        session = Session.objects.get(session_key=session_id)
        user_id = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=user_id)
        return JsonResponse({'username': user.username,
                             'email': user.email,
                             'first_name': user.first_name, 
                             'last_name': user.last_name})
    except (Session.DoesNotExist, KeyError, User.DoesNotExist):
        return JsonResponse({'error': 'Session not found or user does not exist'}, status=400)


@otp_required
def change_password_view(request):
  if request.method == 'POST':
      form = PasswordChangeForm(data=request.POST)
      if form.is_valid():
          # change password
          form.save()
          return redirect('http://localhost:5173/')
  else:
      form = PasswordChangeForm(user=request.user)
  return render(request, 'authentication/change_password.html', {'form': form})