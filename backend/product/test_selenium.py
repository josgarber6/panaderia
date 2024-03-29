from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from base.tests import BaseTestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from base import mods
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os


class ProductSeleniumTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.base = BaseTestCase()

        self.client = APIClient()
        self.token = None
        mods.mock_query(self.client)
        user = User(username='admin', is_superuser=True, is_staff=True)
        user.set_password('qwerty')
        user.save()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def create_category(self):
        self.driver.get(self.live_server_url + "/admin")
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("qwerty")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        self.driver.get(self.live_server_url + "/admin/product/category/add/")
        self.driver.find_element(By.ID, "id_name").send_keys("Test Category")
        self.driver.find_element(By.NAME, "_save").click()

    def test_create_category(self):
        self.driver.get(self.live_server_url + "/admin")
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("qwerty")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        self.driver.get(self.live_server_url + "/admin/product/category/add/")
        self.driver.find_element(By.ID, "id_name").send_keys("Test Category")
        self.driver.find_element(By.NAME, "_save").click()
        self.driver.get(self.live_server_url + "/admin/product/category/")
        self.assertIn("Test Category", self.driver.page_source)

    def test_create_product(self):
        self.create_category()
        self.driver.get(self.live_server_url + "/admin/product/product/add/")
        self.driver.find_element(By.ID, "id_name").send_keys("Test Product")
        self.driver.find_element(By.ID, "id_description").send_keys("Test Description")
        self.driver.find_element(By.ID, "id_price").send_keys("100")

        file_path = os.path.join(os.getcwd(), "backend\media\products\default.jpg")
        self.driver.find_element(By.ID, "id_image").send_keys(file_path)

        self.driver.find_element(By.ID, "id_stock").send_keys("10")
        self.driver.find_element(By.ID, "id_category").send_keys("Test Category")
        self.driver.find_element(By.NAME, "_save").click()
        self.driver.get(self.live_server_url + "/admin/product/product/")
        self.assertIn("Test Product", self.driver.page_source)
        self.assertIn("Test Description", self.driver.page_source)
        self.assertIn("100", self.driver.page_source)
        self.assertIn("10", self.driver.page_source)

        image = self.driver.find_element(By.CLASS_NAME, "field-image").find_element(By.TAG_NAME, "a").get_attribute("href")
        self.assertTrue(image)
        self.assertIn("products/default", image)
        self.assertIn("Test Category", self.driver.page_source)
