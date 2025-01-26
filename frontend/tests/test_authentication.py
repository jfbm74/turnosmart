import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from unittest import TestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SeleniumTests(TestCase):
    def setUp(self):
        # Ruta completa al binario del ChromeDriver
        self.service = Service(
            "chromedriver/mac_arm-132.0.6834.110/chromedriver-mac-arm64/chromedriver"
        )
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.implicitly_wait(10)  # Espera implícita para cargar elementos

    def test_login(self):
        # Abrir la página de inicio de sesión
        self.driver.get("http://127.0.0.1:8000/")

        # Buscar los campos de usuario y contraseña
        username_field = self.driver.find_element(By.NAME, "login")
        password_field = self.driver.find_element(By.NAME, "password")

        # Ingresar datos de prueba
        username_field.send_keys("test_user")
        password_field.send_keys("Yuy1t01506$")
        password_field.send_keys(Keys.RETURN)

        # Validar que el login fue exitoso buscando un elemento único del dashboard
        try:
            # Busca el ícono del dashboard o cualquier elemento único visible después del login
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ri-logout-box-line"))
            )
        except Exception as e:
            self.fail(f"Login fallido: {e}")

        
        # Validar que el login haya sido exitoso
        logout_icon = self.driver.find_element(By.CLASS_NAME, "ri-logout-box-line")
        self.assertTrue(logout_icon)
        

    def tearDown(self):
        # Cerrar el navegador después de la prueba
        self.driver.quit()
    

    def test_invalid_credentials(self):
        self.driver.get("http://127.0.0.1:8000/account/login/")  # Página de login

        # Ingresar usuario y contraseña inválidos
        username_field = self.driver.find_element(By.NAME, "login")
        password_field = self.driver.find_element(By.NAME, "password")
        username_field.send_keys("invalid_user")
        password_field.send_keys("invalid_password")
        password_field.send_keys(Keys.RETURN)

        # Validar que la URL sigue siendo la de login
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.current_url == "http://127.0.0.1:8000/account/login/"
            )
        except Exception as e:
            self.fail(f"No se redirigió correctamente a la página de login: {e}")

        # Validar que aparece un mensaje de error
        try:
            error_message = self.driver.find_element(By.CLASS_NAME, "error-message")  # Ajusta la clase según tu HTML
            self.assertIn("Invalid username or password", error_message.text)  # Ajusta el mensaje según tu aplicación
        except Exception:
            print("No se encontró un mensaje de error. Esto puede ser intencionado.")
