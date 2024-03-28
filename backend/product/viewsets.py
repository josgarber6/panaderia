from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product, Category
from .serializer import ProductSerializer, CategorySerializer
from authentication.models import Customer
from rest_framework.exceptions import PermissionDenied
from django.http import JsonResponse
from rest_framework.decorators import action

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def check_permissions(self, request):
        '''
        Comprueba que el usuario sea administrador y tenga el doble factor de autenticación activado para crear o actualizar un producto.
        '''
        super().check_permissions(request)
        if request.method == 'GET':
            return
        admin_customer = Customer.objects.get(user=request.user)
        if request.method == 'POST':
            if not request.user.is_authenticated or not request.user.is_staff:
                raise PermissionDenied({"detail": "Debe iniciar sesión como administrador para crear un producto."})
            if request.user.is_authenticated and not admin_customer.is_two_factor_enabled():
                raise PermissionDenied({"detail": "Debe activar el doble factor de autenticación para crear un producto."})
        
        if request.method == 'PUT' or request.method == 'PATCH':
            if not request.user.is_authenticated or not request.user.is_staff:
                raise PermissionDenied({"detail": "Debe iniciar sesión como administrador para actualizar un producto."})
            if request.user.is_authenticated and not admin_customer.is_two_factor_enabled():
                raise PermissionDenied({"detail": "Debe activar el doble factor de autenticación para actualizar un producto."})
    
    @action(detail=False, methods=['post'], url_path='check-image', url_name='check-image')
    def check_image(self, request):
        '''
        Comprueba si la imagen del producto es válida.
        '''
        if 'image' in request.data:
            image = request.data['image']
            if image.size > 10*1024*1024:
                return JsonResponse({"title": "size", "detail": "La imagen del producto debe ser menor a 10MB"}, status=status.HTTP_400_BAD_REQUEST)
            if not image.content_type in ['image/jpeg', 'image/png']:
                return JsonResponse({"title": "content_type", "detail": "La imagen del producto debe ser un archivo JPEG o PNG"}, status=status.HTTP_400_BAD_REQUEST)
            images = Product.objects.values_list('image', flat=True)
            result = []
            for img in images:
                img = img.split('/')[-1]
                result.append(img)
            if image.name in result:
                return JsonResponse({'exists': True})
        return JsonResponse({'exists': False}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'image' in request.FILES:
            data['image'] = request.FILES['image']
        else:
            data['image'] = None

        if float(data['price']) <= 0:
            return JsonResponse({"detail": "El precio del producto no puede ser negativo ni cero"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        instance = self.get_object()

        # Comprueba si el stock es menor que 0 y si la categoría no es "Pico" para asignar el valor máximo de un entero de 32 bits.
        if ((instance.stock < 0 or int(data['stock']) < 0) and instance.category.name != "Pico"):
            data['stock'] = 2**31 - 1

        if 'image' in request.FILES:
            instance.image = request.FILES['image']
        else:
            data['image'] = instance.image

        if float(data['price']) <= 0:
            return JsonResponse({"detail": "El precio del producto no puede ser negativo ni cero"}, status=status.HTTP_400_BAD_REQUEST)
        
        if data['category'] == 'null':
            return JsonResponse({"detail": "La categoría del producto es requerida"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def check_permissions(self, request):
        '''
        Comprueba que el usuario sea administrador y tenga el doble factor de autenticación activado para crear o actualizar una categoría.
        '''
        super().check_permissions(request)
        if request.method == 'GET':
            return
        admin_customer = Customer.objects.get(user=request.user)
        if request.method == 'POST':
            if not request.user.is_authenticated or not request.user.is_staff:
                raise PermissionDenied({"detail": "Debe iniciar sesión como administrador para crear una categoría"})
            if request.user.is_authenticated and not admin_customer.is_two_factor_enabled():
                raise PermissionDenied({"detail": "Debe activar el doble factor de autenticación para crear una categoría"})
        
        if request.method == 'PUT' or request.method == 'PATCH':
            if not request.user.is_authenticated or not request.user.is_staff:
                raise PermissionDenied({"detail": "Debe iniciar sesión como administrador para actualizar una categoría"})
            if request.user.is_authenticated and not admin_customer.is_two_factor_enabled():
                raise PermissionDenied({"detail": "Debe activar el doble factor de autenticación para actualizar una categoría"})