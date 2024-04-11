from django.test import TestCase
from .models import Category, Product

class CategoryTestCase(TestCase):
    def setup(self):
      super().setUp()

    def teardown(self):
      super().tearDown()

    def create(self):
      category = Category.objects.create(name="Test Category")
      return category
    
    def test_create_without_persistence(self):
      category = Category(name="Test Category")
      self.assertEqual(str(category), "Test Category")

    def test_create_category(self):
      category = Category.objects.create(name="Test Category")
      self.assertEqual(str(category), "Test Category")

    # Debido al two factor, devuelve un error 403, pero sin el two factor, funciona correctamente.
    def test_create_category_from_api(self):
      response = self.client.post("/api/v1.0/categories/", {"name": "Test Category"})
      self.assertEqual(response.status_code, 201)
      self.assertEqual(response.data["name"], "Test Category")

    def test_get_categories_from_api(self):
      self.create()
      response = self.client.get("/api/v1.0/categories/")
      self.assertEqual(response.status_code, 200)
      self.assertEqual(len(response.data), 1)

    def test_get_category_from_api(self):
      category = self.create()
      response = self.client.get(f"/api/v1.0/categories/{category.id}/")
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.data["name"], "Test Category")
      

class ProductTestCase(TestCase):
    def setup(self):
      super().setUp()

    def teardown(self):
      super().tearDown()

    def create_category(self):
      category = Category.objects.create(name="Test Category")
      return category
    
    def create_product(self):
      product = Product.objects.create(name="Test Product", description="Test Description", price=100, stock=10, category=self.create_category())
      return product
    
    def test_create_without_persistence(self):
      product = Product(name="Test Product", description="Test Description", price=100, stock=10)
      self.assertEqual(str(product), "Test Product")
    
    def test_create_product(self):
      product = self.create_product()
      self.assertEqual(str(product), "Test Product")

    def test_product_category(self):
      category = self.create_category()
      product = self.create_product()
      self.assertEqual(product.category.name, category.name)

    # Debido al two factor, devuelve un error 403, pero sin el two factor, funciona correctamente.
    def test_create_product_from_api(self):
      category = self.create_category()
      product = {"name": "Test Product", "description": "Test Description", "price": 100, "stock": 10, "category": category.id}
      response = self.client.post("/api/v1.0/products/", product)
      self.assertEqual(response.status_code, 201)
      self.assertEqual(response.data["name"], "Test Product")

    def test_get_products_from_api(self):
      self.create_product()
      response = self.client.get("/api/v1.0/products/")
      self.assertEqual(response.status_code, 200)
      self.assertEqual(len(response.data), 1)

    def test_get_product_from_api(self):
      product = self.create_product()
      response = self.client.get(f"/api/v1.0/products/{product.id}/")
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.data["name"], "Test Product")
