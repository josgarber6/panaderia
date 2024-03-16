from django.db import models
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice

class Customer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  address = models.CharField(max_length=255)
  postal_code = models.CharField(max_length=20, default="")

  def __str__(self):
    return "({fName} {lName}, {uName})".format(fName=self.user.first_name, lName=self.user.last_name, uName=self.user.username)
  
  def is_two_factor_enabled(self):
    return TOTPDevice.objects.filter(user=self.user).exists()
