from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Customer
from django import forms

# Formularios de acceso y registro al sistema

class CustomerCreationForm(UserCreationForm):
  username = forms.CharField(
    max_length=127,
    required=True,
    label="Usuario",
    widget=forms.TextInput(
      attrs={
        "placeholder": "Usuario",
        "class": "form-control"
      }
    )
  )
  
  first_name = forms.CharField(
    max_length=20,
    required=True,
    label="Nombre",
    widget=forms.TextInput(
      attrs={
        "placeholder": "Nombre",
        "class": "form-control"
      }
    )
  )

  last_name = forms.CharField(
    max_length=40,
    required=True,
    label="Apellidos",
    widget=forms.TextInput(
      attrs={
        "placeholder": "Apellidos",
        "class": "form-control"
      }
    )
  )

  email = forms.EmailField(
		max_length=254,
		widget=forms.EmailInput(
			attrs={
				"placeholder": "Email",
				"class": "form-control"
			}
		)
	)
  
  address = forms.CharField(
    max_length=254,
    label="Dirección",
    widget=forms.TextInput(
      attrs={
        "placeholder": "Dirección",
        "class": "form-control"
      }
    )
  )

  postal_code = forms.CharField(
    max_length=20,
    required=True,
    label="Código Postal",
    widget=forms.TextInput(
      attrs={
        "placeholder": "Código Postal",
        "class": "form-control"
      }
    )
  )

  password1 = forms.CharField(
    max_length=254,
    min_length=5,
    label="Contraseña",
    widget=forms.PasswordInput(
      attrs={
        "placeholder": "Contraseña",
        "class": "form-control"
      }
    )
  )

  password2 = forms.CharField(
    label="Confirmación Contraseña",
    widget=forms.PasswordInput(
      attrs={
        "placeholder": "Contraseña",
        "class": "form-control"
      }
    )
  )

  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'password1', 'password2')
  
  def save(self, commit=True):
    user = super().save(commit=False)
    user.email = self.cleaned_data["email"]
    user.first_name = self.cleaned_data["first_name"]
    user.last_name = self.cleaned_data["last_name"]
    user.set_password(self.cleaned_data["password1"])
    if commit:
      user.save()
      customer = Customer.objects.create(user=user, address=self.cleaned_data["address"], postal_code=self.cleaned_data["postal_code"])
      customer.save()
    return customer

class PasswordChangeForm(forms.Form):

  old_password = forms.CharField(
    max_length=254,
    min_length=4,
    required=True,
    label="Contraseña Antigua",
    widget=forms.PasswordInput(
      attrs={
        "placeholder": "Contraseña Antigua",
        "class": "form-control",
        "id": "password-input"
      }
    )
  )

  new_password = forms.CharField(
    max_length=254,
    min_length=5,
    label="Nueva Contraseña",
    widget=forms.PasswordInput(
      attrs={
        "placeholder": "Nueva Contraseña",
        "class": "form-control",
        "id": "password-input"
      }
    )
  )

  confirm_new_password = forms.CharField(
    label="Confirmación Nueva Contraseña",
    widget=forms.PasswordInput(
      attrs={
        "placeholder": "Confirmación Nueva Contraseña",
        "class": "form-control",
        "id": "password-input"
      }
    )
  )

  class Meta:
    model = User
    fields = ('old_password', 'new_password', 'confirm_new_password')