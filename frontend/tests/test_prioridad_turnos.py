import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class PrioridadConfigurationTests(unittest.TestCase):
    def setUp(self):
        """Configuración inicial antes de cada prueba"""
        self.service = Service("chromedriver/mac_arm-132.0.6834.110/chromedriver-mac-arm64/chromedriver")
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
    
    def test_crear_prioridad(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/api/turnos/prioridades/")
        driver.find_element(By.CLASS_NAME, "add-btn").click()
        time.sleep(2)
        
        driver.find_element(By.ID, "nombre").send_keys("Alta Urgencia")
        driver.find_element(By.ID, "prioridad").send_keys("ALTA")
        driver.find_element(By.CSS_SELECTOR, "button.btn-success").click()
        
        # Esperar y hacer clic en el botón OK de SweetAlert2
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()
        
        driver.refresh()
        time.sleep(2)
        
        self.assertTrue("Alta Urgencia" in driver.page_source)
    
    def test_editar_prioridad(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/api/turnos/prioridades/")
        driver.find_element(By.CLASS_NAME, "edit-btn").click()
        
        # Esperar que el modal cargue
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "nombre"))
        )
        
        nombre_input = driver.find_element(By.ID, "nombre")
        nombre_input.clear()
        nombre_input.send_keys("Edicion Prioridad")
        driver.find_element(By.CSS_SELECTOR, "button.btn-success").click()
        
        # Esperar y hacer clic en el botón OK de SweetAlert2
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()
        
        driver.refresh()
        time.sleep(2)
        
        self.assertTrue("Edicion Prioridad" in driver.page_source)
    
    def test_eliminar_prioridad(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/api/turnos/prioridades/")
        driver.find_element(By.CLASS_NAME, "delete-btn").click()
        
        # Confirmar eliminación
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()        
        
        
        driver.refresh()
        time.sleep(2)
        
        self.assertFalse("Edicion Prioridad" in driver.page_source)
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
