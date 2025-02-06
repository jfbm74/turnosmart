import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


class HorariosTests(unittest.TestCase):
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

    def test1_agregar_horario(self):
        """Prueba agregar un nuevo Horario"""
        driver = self.driver
        driver.get("http://127.0.0.1:8000/api/horarios/list/")
        
        # Cambiar al tab Horarios
        driver.find_element(By.XPATH, "//a[@href='#schedules']").click()
        time.sleep(2)
        
        driver.find_element(By.ID, "addButton").click()
        time.sleep(2)
        
        # Seleccionar una franja horaria activa
        select_franja = driver.find_element(By.ID, "franja_horaria")
        select_franja.find_elements(By.TAG_NAME, "option")[1].click()
        
        # Seleccionar días activos
        driver.find_element(By.ID, "lunes").click()
        driver.find_element(By.ID, "miercoles").click()
        driver.find_element(By.ID, "viernes").click()
        
        driver.find_element(By.CSS_SELECTOR, "button.btn-success").click()
        
        # Esperar confirmación y refrescar
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()
        
        driver.refresh()
        time.sleep(2)
        
        self.assertTrue("Activo" in driver.page_source)
    
    def test2_editar_horario(self):
        """Prueba editar un Horario existente"""
        driver = self.driver
        driver.get("http://127.0.0.1:8000/api/horarios/list/")
        
        # Cambiar al tab Horarios
        driver.find_element(By.XPATH, "//a[@href='#schedules']").click()
        time.sleep(2)
        
        driver.find_element(By.CLASS_NAME, "edit-btn").click()
        
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "franja_horaria"))
        )
        
        # Modificar días activos
        driver.find_element(By.ID, "martes").click()
        driver.find_element(By.ID, "jueves").click()
        
        driver.find_element(By.CSS_SELECTOR, "button.btn-success").click()
        
        # Confirmar y refrescar
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()
        
        driver.refresh()
        time.sleep(2)
        
        self.assertTrue("Activo" in driver.page_source)
    
    def test3_eliminar_horario(self):
        """Prueba eliminar un Horario"""
        driver = self.driver
        driver.get("http://127.0.0.1:8000/api/horarios/list/")
        
        # Cambiar al tab Horarios
        driver.find_element(By.XPATH, "//a[@href='#schedules']").click()
        time.sleep(2)
        
        # Verificar si hay al menos un horario antes de intentar eliminar
        elementos_horario = driver.find_elements(By.CLASS_NAME, "delete-btn")
        if not elementos_horario:
            self.skipTest("No hay horarios disponibles para eliminar")
        
        elementos_horario[0].click()
        
        # Confirmar eliminación
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()
        
        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        
        # Verificar que la lista de horarios ya no contenga el elemento eliminado
        elementos_actualizados = driver.find_elements(By.CLASS_NAME, "delete-btn")
        self.assertLess(len(elementos_actualizados), len(elementos_horario), "El horario no fue eliminado correctamente")
    
    def tearDown(self):
        self.driver.quit()

