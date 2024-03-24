from datetime import datetime
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(null=True, upload_to='products/')
    highlighted = models.BooleanField(default=False)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category,
                                 on_delete= models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name='products')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']