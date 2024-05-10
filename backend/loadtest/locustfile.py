from auth import admin_login, customer_login, logout

from locust import (
    HttpUser,
    SequentialTaskSet,
    task,
    between
)


HOST = "http://localhost:8000"

class CustomerTaskSet(SequentialTaskSet):
    def on_start(self):
        admin_login(self)

    def on_stop(self):
        logout(self)

    @task
    def get_customers(self):
        self.client.get(HOST + "/account/customers/")

    @task
    def post_customer(self):
        json_data = {
            "user": "1",
            "address": "123 Main St",
            "postal_code": "12345",
        }
        self.client.post(HOST + "/account/customers/", json=json_data)

class ProductTaskSet(SequentialTaskSet):

    @task
    def get_products(self):
        customer_login(self)
        self.client.get(HOST + "/api/v1.0/products/")
        self.client.post(HOST + "/account/logout/")

    @task
    def post_product(self):
        admin_login(self)
        json_data = {
            "name": "Product Name",
            "description": "Product Description",
            "price": "9.99",
            "stock": "100",
            "category": "1",
            "image": "image.jpg",
        }
        self.client.post(HOST + "/api/v1.0/products/", json=json_data)
        self.client.post(HOST + "/account/logout/")

    @task
    def put_product(self):
        admin_login(self)
        json_data = {
            "name": "Product Name Updated",
            "description": "Product Description Updated",
            "stock": 10,
            "category": "1",
            "price": 9.99,
            "image": "image.jpg",
        }
        self.client.put(HOST + "/api/v1.0/products/1/", json=json_data)
        self.client.post(HOST + "/account/logout/")

    @task
    def delete_product(self):
        admin_login(self)
        self.client.delete(HOST + "/api/v1.0/products/1/")
        self.client.post(HOST + "/account/logout/")

class OrderTaskSet(SequentialTaskSet):
    @task
    def get_orders(self):
        admin_login(self)
        self.client.get(HOST + "/api/v1.0/orders/")

    @task
    def get_my_orders(self):
        customer_login(self)
        self.client.get(HOST + "/api/v1.0/orders/my_orders/")
        self.client.post(HOST + "/account/logout/")

    @task
    def put_order(self):
        admin_login(self)
        json_data = {
            "shipping_status": "Entregado",
        }
        self.client.put(HOST + "/api/v1.0/orders/", json=json_data)

    @task
    def delete_order(self):
        admin_login(self)
        self.client.delete("/api/v1.0/orders/")

class CategoryTaskSet(SequentialTaskSet):
    @task
    def get_categories(self):
        self.client.get("/api/v1.0/categories/")

    @task
    def post_category(self):
        admin_login(self)
        self.client.post("/api/v1.0/categories/", json={"name": "Prueba"})

    @task
    def put_category(self):
        admin_login(self)
        categories = self.client.get("/api/v1.0/categories/")
        category = categories.json()[-1]
        self.client.put("/api/v1.0/categories/" + str(category["id"]) + "/", json={"name": "Prueba2"})

    @task
    def delete_category(self):
        admin_login(self)
        categories = self.client.get("/api/v1.0/categories/")
        category = categories.json()[-1]
        self.client.delete("/api/v1.0/categories/" + str(category["id"]) + "/")

class CustomerUser(HttpUser):
    host = HOST
    tasks = [CustomerTaskSet]
    wait_time = between(3, 5)

class ProductUser(HttpUser):
    host = HOST
    tasks = [ProductTaskSet]
    wait_time = between(3, 5)

class OrderUser(HttpUser):
    host = HOST
    tasks = [OrderTaskSet]
    wait_time = between(3, 5)

class CategoryUser(HttpUser):
    host = HOST
    tasks = [CategoryTaskSet]
    wait_time = between(3, 5)