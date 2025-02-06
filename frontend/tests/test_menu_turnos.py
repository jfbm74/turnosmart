import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MenusTests(unittest.TestCase):
    def setUp(self):
        """Configuración inicial antes de cada prueba"""
        self.service = Service("chromedriver/mac_arm-132.0.6834.110/chromedriver-mac-arm64/chromedriver")
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.implicitly_wait(10)
        self.login()

    def login(self):
        """Helper method para hacer login y mantener la sesión"""
        self.driver.get("http://127.0.0.1:8000/")
        username_field = self.driver.find_element(By.NAME, "login")
        password_field = self.driver.find_element(By.NAME, "password")
        username_field.send_keys("test_user")
        password_field.send_keys("Yuy1t01506$")
        password_field.send_keys(Keys.RETURN)
        
        # Esperar a que la sesión se establezca
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ri-logout-box-line"))
        )
        
        # Recargar la página para asegurar que la sesión se mantenga
        self.driver.get("http://127.0.0.1:8000/api/menu/list/")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "add-btn"))
        )

    def test_agregar_menu(self):
        """Prueba agregar un nuevo Menú"""
        driver = self.driver
        
        driver.find_element(By.CLASS_NAME, "add-btn").click()
        time.sleep(2)
        
        driver.find_element(By.ID, "nombre").send_keys("Menú de Prueba")
        tipo_select = driver.find_element(By.ID, "tipo")
        tipo_select.find_elements(By.TAG_NAME, "option")[0].click()
        
        # Seleccionar la primera prioridad disponible si existe
        select_prioridad = driver.find_element(By.ID, "prioridad")
        opciones_prioridad = select_prioridad.find_elements(By.TAG_NAME, "option")
        if len(opciones_prioridad) > 1:
            opciones_prioridad[1].click()
        
        # Esperar a que el botón sea visible y clickeable antes de hacer clic
        guardar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "boton-guardar"))
        )
        guardar_btn.click()
        
        # Esperar confirmación de éxito y hacer clic en OK
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()
        
        driver.refresh()
        time.sleep(2)
        
        # Esperar a que el menú aparezca en la tabla
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Menú de Prueba')]"))
        )
        
        self.assertTrue("Menú de Prueba" in driver.page_source)
    
    def test_editar_menu(self):
        """Prueba editar un Menú existente"""
        driver = self.driver
        
        driver.find_element(By.CLASS_NAME, "edit-btn").click()
        
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "nombre"))
        )
        
        nombre_input = driver.find_element(By.ID, "nombre")
        nombre_input.clear()
        nombre_input.send_keys("Menú Editado")
        
        # Esperar a que el botón sea visible y clickeable antes de hacer clic
        guardar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "boton-guardar"))
        )
        guardar_btn.click()
        
        # Confirmar y refrescar
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()
        
        driver.refresh()
        time.sleep(2)
        
        self.assertTrue("Menú Editado" in driver.page_source)
    
    def test_eliminar_menu(self):
        """Prueba eliminar un Menú"""
        driver = self.driver
        driver.get("http://127.0.0.1:8000/api/menu/list/")
        
        # Buscar y hacer clic en el botón eliminar por ID
        eliminar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "boton-eliminar"))
        )
        eliminar_btn.click()
        
        # Confirmar eliminación en SweetAlert2
        confirm_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        )
        confirm_btn.click()
        
        # Esperar un tiempo para permitir que la eliminación se procese en el backend
        time.sleep(3)
        
        # Refrescar la página para verificar la eliminación
        driver.refresh()
        time.sleep(3)
        
        # Intentar localizar el menú nuevamente
        elementos_menu = driver.find_elements(By.XPATH, "//td[contains(text(), 'Menú Editado')]")
        self.assertEqual(len(elementos_menu), 0, "El menú sigue presente en la página después de la eliminación")
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
