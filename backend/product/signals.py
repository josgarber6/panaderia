import os
from django.db import models
from django.dispatch import receiver
from .models import Product

@receiver(models.signals.post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    print(f"Post delete signal for Product {instance.id}")
    if instance.image:
        print(f"Product has an image at {instance.image.path}")
        if os.path.isfile(instance.image.path):
            print("Image file exists, attempting to delete")
            os.remove(instance.image.path)
            print("Image file deleted")
        else:
            print("Image file does not exist")
    else:
        print("Product does not have an image")

@receiver(models.signals.pre_save, sender=Product)
def auto_delete_file_on_change(sender, instance, **kwargs):
    print(f"Pre save signal for Product {instance.id}")
    if not instance.id:
        return False

    try:
        old_file = Product.objects.get(pk=instance.pk).image
    except Product.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if old_file and os.path.isfile(old_file.path):
            os.remove(old_file.path)
            print("Old image file deleted")
        else:
            print("Old image file does not exist")
    else:
        print("Old image file is the same as the new image file")