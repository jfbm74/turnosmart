import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time


class TramiteTests(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.base_url = "http://127.0.0.1:8000"
        
    def login(self):
        """Helper method para hacer login antes de las pruebas"""
        self.driver.get(self.base_url + "/")
        username_field = self.driver.find_element(By.NAME, "login")
        password_field = self.driver.find_element(By.NAME, "password")
        username_field.send_keys("test_user")
        password_field.send_keys("Yuy1t01506$")
        password_field.send_keys(Keys.RETURN)
        
        # Esperar a que aparezca un elemento que indique login exitoso
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ri-logout-box-line"))
        )
    
    def safe_click(self, by, value, timeout=10, retries=3):
        """Método seguro para hacer clic evitando StaleElementReferenceException"""
        for _ in range(retries):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((by, value))
                )
                element.click()
                return
            except StaleElementReferenceException:
                print(f"Elemento {value} obsoleto, reintentando...")
        raise Exception(f"No se pudo hacer clic en {value} después de {retries} intentos.")

        
    def test_crear_tramite(self):
        """Prueba para crear un nuevo trámite"""
        self.login()
        self.driver.get(self.base_url + "/api/core/tramites/")
        
        # Click en el botón de agregar trámite
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "add-btn"))
        ).click()
        
        # Esperar a que el modal esté visible
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "tramiteForm"))
        )
        
        # Llenar el formulario
        self.driver.find_element(By.ID, "nombre").send_keys("Trámite de prueba")
        self.driver.find_element(By.ID, "iniciales").send_keys("TP")
        
        # Seleccionar opciones en los selects
        Select(self.driver.find_element(By.ID, "cliente_requerido")).select_by_value("atender")
        Select(self.driver.find_element(By.ID, "ventanilla_atencion")).select_by_index(1)
        
        # Seleccionar múltiples opciones en ventanilla_transferencia_frecuente
        ventanilla_select = Select(self.driver.find_element(By.ID, "ventanilla_transferencia_frecuente"))
        ventanilla_options = ventanilla_select.options
        if len(ventanilla_options) > 1:
            ventanilla_select.select_by_index(0)
            ventanilla_select.select_by_index(1)
        
        # Esperar a que el botón guardar sea interactuable y hacer clic
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "guardar-tramite"))
        ).click()
        
        # Esperar y hacer clic en el botón de confirmación de SweetAlert2
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()
        
        # Verificar que el trámite aparece en la tabla
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, "//td[contains(text(), 'Trámite de prueba')]"), "Trámite de prueba")
        )

    def test_editar_tramite(self):
        """Prueba para editar un trámite existente"""
        self.login()
        self.driver.get(self.base_url + "/api/core/tramites/")
        
        # Click en el botón de edición del primer trámite
        edit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "edit-btn"))
        )
        edit_button.click()
        
        # Esperar a que el modal esté visible
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "tramiteForm"))
        )
        
        # Modificar nombre
        nombre_field = self.driver.find_element(By.ID, "nombre")
        nombre_field.clear()
        nombre_field.send_keys("Trámite Modificado")
        
        # Modificar selección en los selects
        Select(self.driver.find_element(By.ID, "cliente_requerido")).select_by_value("turno")
        Select(self.driver.find_element(By.ID, "ventanilla_atencion")).select_by_index(2)
        
        # Esperar a que el botón guardar sea interactuable y hacer clic
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "guardar-tramite"))
        ).click()
        
        # Esperar y hacer clic en el botón de confirmación de SweetAlert2
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()
        
        # Verificar que el cambio se reflejó
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, "//td[contains(text(), 'Trámite Modificado')]"), "Trámite Modificado")
        )    

    

    def test_eliminar_tramite(self):
        """Prueba para eliminar un trámite"""
        self.login()
        self.driver.get(self.base_url + "/api/core/tramites/")
        
        # Click en el botón de eliminación
        #self.safe_click(self.driver, By.CLASS_NAME, "delete-btn")
        self.safe_click(By.CLASS_NAME, "delete-btn")


        # Esperar confirmación de SweetAlert2 y hacer clic en el botón de confirmación
        self.safe_click(By.CLASS_NAME, "swal2-confirm")

        # Esperar 2 segundos para estabilizar el DOM antes del siguiente clic
        time.sleep(2)

        # Hacer clic en el botón OK del mensaje de éxito de SweetAlert2
        self.safe_click(By.CLASS_NAME, "swal2-confirm")

        
        # Verificar que el trámite desaparece después de la eliminación
        WebDriverWait(self.driver, 10).until_not(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Trámite Modificado')]"))
        )


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
