from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'

    # Importar el archivo signals que comprueba si un producto tiene una imagen asociada y la elimina del sistema de archivos cuando se elimina el producto.
    def ready(self):
        import product.signals
