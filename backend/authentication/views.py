from django.shortcuts import render, redirect, resolve_url
from .forms import PasswordChangeForm
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
        context['home_url'] = resolve_url(settings.FRONTEND_BASE_URL)
        return context
    
def logout_view(request):
  logout(request)
  # Eliminar el sessionid de las cookies
  request.COOKIES.clear()
  response = redirect(settings.LOGOUT_REDIRECT_URL)
  # Eliminar el csrftoken de las cookies
  response.set_cookie('csrftoken', '', max_age=0)
  return response


def get_username_from_session(request):
    try:
        session_id = request.COOKIES['sessionid']
        session = Session.objects.get(session_key=session_id)
        user_id = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=user_id)
        if user.is_superuser or user.is_staff:
            if(Customer.objects.filter(user=user).count() == 0):
                # Create customer if it doesn't exist
                admin_customer = Customer.objects.create(user=user)
                admin_customer.save()
            admin_customer = Customer.objects.get(user=user)
            return JsonResponse({'username': user.username,
                                 'email': user.email,
                                 'first_name': user.first_name, 
                                 'last_name': user.last_name,
                                 'isTwoFactorEnabled': admin_customer.is_two_factor_enabled(),
                                 'isAdmin': True})
        else:
            customer = Customer.objects.get(user=user)
            return JsonResponse({'username': user.username,
                             'email': user.email,
                             'first_name': user.first_name, 
                             'last_name': user.last_name,
                             'isTwoFactorEnabled': customer.is_two_factor_enabled()})
    except (Session.DoesNotExist, KeyError):
        return JsonResponse({'detail': 'User is not authenticated'})
    except (Customer.DoesNotExist):
        return JsonResponse({'error': 'Customer does not exist'}, status=400)
    
def get_user_info(request, userId):
    try:
        user = User.objects.get(pk=userId)
        return JsonResponse({'username': user.username,
                                'email': user.email,
                                'first_name': user.first_name, 
                                'last_name': user.last_name,
                            })
    except (KeyError, User.DoesNotExist):
        return JsonResponse({'error': 'User does not exist'}, status=400)


@otp_required
def change_password_view(request):
  if request.method == 'POST':
      form = PasswordChangeForm(request.POST)
      if form.is_valid():
          # change password
        old_password = form.cleaned_data.get('old_password')
        new_password = form.cleaned_data.get('new_password')
        user = request.user
        try:
            check_password = user.check_password(old_password)
        except NotImplementedError:
            check_password = False
        if not check_password:
            form.add_error('old_password', 'Contraseña antigua incorrecta')
            return render(request, 'authentication/change_password.html', {'form': form})
        if new_password == old_password:
            form.add_error('new_password', 'La nueva contraseña no puede ser igual a la anterior')
            return render(request, 'authentication/change_password.html', {'form': form})
        if new_password != form.cleaned_data.get('confirm_new_password'):
            form.add_error('confirm_new_password', 'Las contraseñas no coinciden')
            return render(request, 'authentication/change_password.html', {'form': form})
        user.set_password(new_password)
        user.save()
        return change_password_done_view(request)
  else:
      form = PasswordChangeForm()
  return render(request, 'authentication/change_password.html', {'form': form, 'home_url': settings.FRONTEND_BASE_URL})

def change_password_done_view(request):
    login = resolve_url(settings.LOGIN_URL)
    logout(request)
    return render(request, 'authentication/change_password_done.html', {'login': login})