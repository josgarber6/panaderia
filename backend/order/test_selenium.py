from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from base.tests import BaseTestCase
from rest_framework.test import APIClient
from base import mods
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from decouple import config

class OrderSeleniumTestCase(StaticLiveServerTestCase):
  def setUp(self):
    self.base = BaseTestCase()

    self.client = APIClient()
    self.token = None
    mods.mock_query(self.client)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    super().setUp()

  def tearDown(self):
    super().tearDown()
    self.driver.quit()

    self.base.tearDown()

  def login(self):
    self.driver.get(config("FRONTEND_BASE_URL"))
    self.driver.find_element(By.ID, "login").click()
    self.driver.find_element(By.NAME, "auth-username").send_keys("prueba2")
    self.driver.find_element(By.NAME, "auth-password").send_keys("contra123")
    self.driver.find_element(By.CLASS_NAME, "btn-primary").click()

  def login_and_2fa(self):
    self.driver.get(config("FRONTEND_BASE_URL"))
    self.driver.find_element(By.ID, "login").click()
    self.driver.find_element(By.NAME, "auth-username").send_keys("drkenobi")
    self.driver.find_element(By.NAME, "auth-password").send_keys("contra123")
    self.driver.find_element(By.CLASS_NAME, "btn-primary").click()

    self.driver.find_element(By.NAME, "token-otp_token").click()
    WebDriverWait(self.driver, 100).until(lambda s: s.find_element(By.NAME, "token-otp_token").get_attribute("value") != "")
    self.driver.find_element(By.CLASS_NAME, "btn-primary").click()

  def test_create_order(self):
    
    self.login_and_2fa()

    # Seleccionar un producto y añadirlo al carrito
    self.driver.find_element(By.XPATH, "//a[contains(text(),'Productos')]").click()
    WebDriverWait(self.driver, 10).until(lambda s: s.find_element(By.ID, "quantity-4").is_displayed())
    self.driver.find_element(By.ID, "quantity-4").clear()
    self.driver.find_element(By.ID, "quantity-4").send_keys("10")
    self.driver.find_element(By.ID, "add-to-cart-4").click()

    self.driver.find_element(By.XPATH, '//a[@href="/cart"]').click()
    self.driver.find_element(By.CLASS_NAME, "btn-success").click()
    self.driver.find_element(By.ID, "confirm-order").click()

    # Pago con Stripe
    WebDriverWait(self.driver, 10).until(lambda s: s.current_url.startswith("https://checkout.stripe.com/c/pay/"))
    self.assertTrue(self.driver.current_url.startswith("https://checkout.stripe.com/c/pay/"))
    self.driver.find_element(By.ID, "email").send_keys("drkenobi27@gmail.com")

    # Si aparece el cuadro de diálogo de verificación de enlace, cerrarlo
    WebDriverWait(self.driver, 10).until(lambda s: s.find_element(By.CLASS_NAME, "LinkVerificationBody"))
    if (self.driver.find_element(By.CLASS_NAME, "LinkVerificationBody")):
      self.driver.find_element(By.CLASS_NAME, "Button--secondary").click()

    self.driver.find_element(By.ID, "cardNumber").send_keys("4242424242424242")
    self.driver.find_element(By.ID, "cardExpiry").send_keys("0424")
    self.driver.find_element(By.ID, "cardCvc").send_keys("242")
    self.driver.find_element(By.ID, "billingName").send_keys("Jose Maria")
    self.driver.find_element(By.CLASS_NAME, "SubmitButton-IconContainer").click()

    # Comprobar que se ha completado el pago
    WebDriverWait(self.driver, 10).until(lambda s: s.current_url.startswith(config("FRONTEND_BASE_URL") + "payment/completed"))
    self.assertTrue(self.driver.current_url.startswith(config("FRONTEND_BASE_URL") + "payment/completed"))
    self.assertTrue(self.driver.find_element(By.XPATH, "//h1[contains(text(),'¡Pago completado!')]").is_displayed())

    # Verificar que el pedido se ha creado
    self.driver.find_element(By.XPATH, "//a[contains(text(),'este enlace')]").click()
    WebDriverWait(self.driver, 10).until(lambda s: "Pedido" in s.find_element(By.TAG_NAME, "h3").text)
    self.assertTrue(self.driver.current_url.startswith(config("FRONTEND_BASE_URL") + "order/my_orders"))
    self.assertTrue("Pedido" in self.driver.find_element(By.TAG_NAME, "h3").text)

  def test_create_order_without_login(self):
    # Seleccionar un producto y añadirlo al carrito
    self.driver.get(config("FRONTEND_BASE_URL"))
    self.driver.find_element(By.XPATH, "//a[contains(text(),'Productos')]").click()
    WebDriverWait(self.driver, 10).until(lambda s: s.find_element(By.ID, "quantity-4").is_displayed())
    self.driver.find_element(By.ID, "quantity-4").clear()
    self.driver.find_element(By.ID, "quantity-4").send_keys("10")
    self.driver.find_element(By.ID, "add-to-cart-4").click()

    self.driver.find_element(By.XPATH, '//a[@href="/cart"]').click()
    self.driver.find_element(By.CLASS_NAME, "btn-success").click()

    self.assertIn("Debe iniciar sesión y activar el doble factor de autenticación para realizar un pedido.", self.driver.find_element(By.ID, "error-message").text)

  def test_create_order_without_2fa(self):
    self.login()

    # Seleccionar un producto y añadirlo al carrito
    self.driver.find_element(By.XPATH, "//a[contains(text(),'Productos')]").click()
    WebDriverWait(self.driver, 10).until(lambda s: s.find_element(By.ID, "quantity-4").is_displayed())
    self.driver.find_element(By.ID, "quantity-4").clear()
    self.driver.find_element(By.ID, "quantity-4").send_keys("10")
    self.driver.find_element(By.ID, "add-to-cart-4").click()

    self.driver.find_element(By.XPATH, '//a[@href="/cart"]').click()
    self.driver.find_element(By.CLASS_NAME, "btn-success").click()

    self.assertIn("Debe activar el doble factor de autenticación para realizar un pedido.", self.driver.find_element(By.ID, "error-message").text)

  def test_create_order_cash(self):
    self.login_and_2fa()

    # Seleccionar un producto y añadirlo al carrito
    self.driver.find_element(By.XPATH, "//a[contains(text(),'Productos')]").click()
    WebDriverWait(self.driver, 10).until(lambda s: s.find_element(By.ID, "quantity-4").is_displayed())
    self.driver.find_element(By.ID, "quantity-4").clear()
    self.driver.find_element(By.ID, "quantity-4").send_keys("10")
    self.driver.find_element(By.ID, "add-to-cart-4").click()

    self.driver.find_element(By.XPATH, '//a[@href="/cart"]').click()
    self.driver.find_element(By.CLASS_NAME, "btn-success").click()

    self.driver.find_element(By.ID, "payment").click()
    self.driver.find_element(By.XPATH, "//option[contains(text(),'Pago en Efectivo')]").click()
    self.driver.find_element(By.ID, "confirm-order").click()

    WebDriverWait(self.driver, 10).until(lambda s: s.current_url.startswith(config("FRONTEND_BASE_URL") + "order/completed"))
    self.assertTrue(self.driver.current_url.startswith(config("FRONTEND_BASE_URL") + "order/completed"))
    self.assertIn("¡Pedido realizado!", self.driver.find_element(By.TAG_NAME, "h1").text)
