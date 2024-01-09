from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  address = models.CharField(max_length=255)

  def __str__(self):
    return "({fName} {lName}, {uName})".format(fName=self.user.first_name, lName=self.user.last_name, uName=self.user.username)