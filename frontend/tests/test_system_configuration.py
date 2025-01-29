import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from unittest import TestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class SystemConfigurationTests(TestCase):
    def setUp(self):
        """Configuración inicial antes de cada prueba"""
        self.service = Service(
            "chromedriver/mac_arm-132.0.6834.110/chromedriver-mac-arm64/chromedriver"
        )
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.implicitly_wait(10)
        self.login()
        
    def login(self):
        """Helper method para hacer login"""
        self.driver.get("http://127.0.0.1:8000/")
        username_field = self.driver.find_element(By.NAME, "login")
        password_field = self.driver.find_element(By.NAME, "password")
        username_field.send_keys("test_user")
        password_field.send_keys("Yuy1t01506$")
        password_field.send_keys(Keys.RETURN)
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ri-logout-box-line"))
        )

    def click_submit_button(self):
        """Helper method para hacer clic en el botón submit"""
        try:
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btnGuardarCambios"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", submit_button)
        except TimeoutException:
            self.fail("No se pudo encontrar o hacer clic en el botón de guardado")

    def navigate_to_system_config(self):
        """Helper method para navegar a la página de configuración"""
        self.driver.get("http://127.0.0.1:8000/api/configuracion/sistemas/")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "systemConfigForm"))
        )

    def test_save_configuration(self):
        """Prueba el guardado exitoso de la configuración"""
        # Esta prueba verifica que se pueden guardar cambios en el formulario
        self.navigate_to_system_config()
        
        # Modificar varios campos
        tiempo_espera = self.driver.find_element(By.ID, "tiempo_espera")
        tiempo_espera.clear()
        tiempo_espera.send_keys("15")
        
        umbral_espera = self.driver.find_element(By.ID, "umbral_espera")
        umbral_espera.clear()
        umbral_espera.send_keys("7")
        
        # Guardar cambios
        self.click_submit_button()
        
        # Verificar mensaje de éxito
        try:
            alert = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
            )
            self.assertTrue(alert.is_displayed())
        except TimeoutException:
            self.fail("No se mostró el mensaje de éxito")

    def test_required_fields(self):
        """Prueba la validación de campos requeridos"""
        self.navigate_to_system_config()
        
        # Limpiar campos requeridos
        campos_requeridos = ["tiempo_espera", "umbral_espera", 
                        "num_max_turnos_cedula", "digitos_max_cedula_turnero"]
        for campo in campos_requeridos:
            element = self.driver.find_element(By.ID, campo)
            element.clear()
        
        # Intentar guardar
        self.click_submit_button()
        
        # Verificar mensaje de error
        try:
            alert = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-container"))
            )
            error_text = self.driver.find_element(By.CLASS_NAME, "swal2-html-container").text
            self.assertIn("Por favor complete los siguientes campos", error_text)
            # Verificar que se mencionan los campos específicos
            for campo in campos_requeridos:
                campo_formateado = campo.replace("_", " ")
                self.assertIn(campo_formateado, error_text.lower())
        except TimeoutException:
            self.fail("No se mostró el mensaje de error")

    def test_notification_settings(self):
        """Prueba la configuración de notificaciones"""
        # Esta prueba verifica la sección de notificaciones
        self.navigate_to_system_config()
        
        # Configurar campos de notificación
        email = self.driver.find_element(By.ID, "email_notificaciones")
        host = self.driver.find_element(By.ID, "host_notificaciones")
        puerto = self.driver.find_element(By.ID, "puerto_notificaciones")
        
        email.clear()
        email.send_keys("test@example.com")
        host.clear()
        host.send_keys("smtp.test.com")
        puerto.clear()
        puerto.send_keys("587")
        
        # Guardar cambios
        self.click_submit_button()
        
        # Verificar mensaje de éxito
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
            )
        except TimeoutException:
            self.fail("No se guardó la configuración de notificaciones")

    def test_default_values(self):
        """Prueba que se carguen los valores por defecto"""
        # Esta prueba verifica que los valores por defecto se carguen correctamente
        self.navigate_to_system_config()
        
        # Verificar valores por defecto
        tiempo_espera = self.driver.find_element(By.ID, "tiempo_espera")
        version = self.driver.find_element(By.ID, "version_sistema")
        
        self.assertIsNotNone(tiempo_espera.get_attribute("value"))
        self.assertEqual(version.get_attribute("value"), "1.0.0")

    def tearDown(self):
        """Limpieza después de cada prueba"""
        if self.driver:
            self.driver.quit()