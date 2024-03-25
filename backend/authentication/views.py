from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from .forms import CustomerCreationForm
from django.views.generic import TemplateView
from django_otp.decorators import otp_required
from django.conf import settings
# Session cookies
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from .models import Customer
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
    return render(request, 'authentication/signup.html', {'form': form, 'home_url': settings.FRONTEND_BASE_URL})

class SignupCompleteView(TemplateView):
    template_name = 'authentication/signup_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['two_factor_setup_url'] = resolve_url(settings.TWO_FACTOR_SETUP_URL)
        context['home_url'] = settings.FRONTEND_BASE_URL
        return context
    
def logout_view(request):
  logout(request)
  return redirect(settings.LOGOUT_REDIRECT_URL)


def get_username_from_session(request):
    session_id = request.COOKIES['sessionid']
    try:
        session = Session.objects.get(session_key=session_id)
        user_id = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=user_id)
        customer = Customer.objects.get(user=user)
        return JsonResponse({'username': user.username,
                             'email': user.email,
                             'first_name': user.first_name, 
                             'last_name': user.last_name,
                             'isTwoFactorEnabled': customer.is_two_factor_enabled()})
    except (Session.DoesNotExist, KeyError, User.DoesNotExist):
        return JsonResponse({'error': 'Session not found or user does not exist'}, status=400)


@otp_required
def change_password_view(request):
  if request.method == 'POST':
      form = PasswordChangeForm(data=request.POST)
      if form.is_valid():
          # change password
          form.save()
          return redirect(settings.LOGIN_REDIRECT_URL)
  else:
      form = PasswordChangeForm(user=request.user)
  return render(request, 'authentication/change_password.html', {'form': form})