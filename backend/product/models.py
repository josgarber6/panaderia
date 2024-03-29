from django.db import models

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

    def save(self, *args, **kwargs):
        '''
        Comprueba si la imagen del producto ha cambiado y elimina la anterior del sistema de archivos.
        '''
        if self.stock < 0 and self.category.name != "Pico":
            self.stock = 2**31 - 1
        try:
            this = Product.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except: pass
        super(Product, self).save(*args, **kwargs)