import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException # ADDED this import
from selenium.webdriver.common.action_chains import ActionChains

class FranjaHorariaTests(unittest.TestCase):
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

    def test1_agregar_franja_horaria(self):
        """Prueba agregar una nueva Franja Horaria"""
        driver = self.driver
        driver.get("http://127.0.0.1:8000/api/horarios/list/")

        # Cambiar al tab Franjas Horarias
        tab_franjas = driver.find_element(By.XPATH, "//a[@href='#timeslots']")
        driver.execute_script("arguments[0].click();", tab_franjas)
        time.sleep(2)

        driver.find_element(By.ID, "addButton").click()
        time.sleep(2)

        # Diligenciar el formulario y guardar
        driver.find_element(By.ID, "hora_inicio").send_keys("08:00AM")
        driver.find_element(By.ID, "hora_fin").send_keys("10:00AM")
        driver.find_element(By.ID, "guardar-franja-horaria").click()

        # Esperar confirmación SweetAlert y hacer clic en OK
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()

        # Esperar a que el SweetAlert desaparezca (importante!)
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "swal2-container"))
        )

        # Cambiar de nuevo al tab de Franjas Horarias
        tab_franjas = driver.find_element(By.XPATH, "//a[@href='#timeslots']")
        driver.execute_script("arguments[0].click();", tab_franjas)
        time.sleep(2)

         # Wait for a longer period for the table to load after the SweetAlert.
        time.sleep(5)

        # Verificar que el horario creado existe
        try:
            # Verificar primero la existencia de la fila por su ID *
            # Esto necesita un ajuste: No tenemos forma directa de obtener el ID del nuevo elemento.
            # Tendremos que obtenerlo de la respuesta de la creación.
            # Por ahora, asumimos que se crea al final y buscamos el último.
            row = WebDriverWait(driver, 10).until(
               EC.presence_of_element_located((By.XPATH, "//tbody[@id='franjas-horarias-table-body']/tr[last()]"))
            )
            # Luego, verifica que la información sea la correcta
            assert "8 a.m." in row.text and "10 a.m." in row.text, "Los datos de hora no coinciden"

        except TimeoutException:
            self.fail("Franja horaria no encontrada después de la creación")

    
    def test2_editar_franja_horaria(self):
        """Prueba editar una Franja Horaria existente"""
        driver = self.driver
        driver.get("http://127.0.0.1:8000/api/horarios/list/")
        
        # Cambiar al tab Franjas Horarias
        tab_franjas = driver.find_element(By.XPATH, "//a[@href='#timeslots']")
        driver.execute_script("arguments[0].click();", tab_franjas)
        time.sleep(2)
        
        # Encuentra el botón de editar *del último horario*
        edit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//tbody[@id='franjas-horarias-table-body']/tr[last()]/td/div/button[contains(@class, 'edit-btn')]"))
        )
        edit_button.click()

        # Espera a que el modal de edición esté visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "hora_inicio"))
        )
        
        # Borrar y rellenar el campo de hora de inicio con el nuevo valor
        hora_inicio_input = driver.find_element(By.ID, "hora_inicio")
        hora_inicio_input.clear()
        hora_inicio_input.send_keys("09:00AM")

        # Borrar y rellenar el campo de hora de inicio con el nuevo valor
        hora_inicio_input = driver.find_element(By.ID, "hora_fin")
        hora_inicio_input.clear()
        hora_inicio_input.send_keys("11:00AM")

        # Guardar los cambios
        driver.find_element(By.ID, "guardar-franja-horaria").click()

        # Esperar confirmación SweetAlert y hacer clic en OK
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()

        # Esperar a que el SweetAlert desaparezca
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "swal2-container"))
        )
        
        # Cambiar de nuevo al tab de Franjas Horarias
        tab_franjas = driver.find_element(By.XPATH, "//a[@href='#timeslots']")
        driver.execute_script("arguments[0].click();", tab_franjas)
        time.sleep(2)

        # Verificar que la hora de inicio se haya actualizado correctamente.

        """ try:
            WebDriverWait(driver, 10).until(
                 EC.presence_of_element_located((By.XPATH, "//tbody[@id='franjas-horarias-table-body']/tr[last()]/td[contains(text(), '9 a.m.')]"))
            )
        except TimeoutException:
            self.fail("La franja horaria no se actualizó correctamente") """
        
        try:
            # Verificar primero la existencia de la fila por su ID *
            # Esto necesita un ajuste: No tenemos forma directa de obtener el ID del nuevo elemento.
            # Tendremos que obtenerlo de la respuesta de la creación.
            # Por ahora, asumimos que se crea al final y buscamos el último.
            row = WebDriverWait(driver, 10).until(
               EC.presence_of_element_located((By.XPATH, "//tbody[@id='franjas-horarias-table-body']/tr[last()]"))
            )
            # Luego, verifica que la información sea la correcta
            assert "9 a.m." in row.text and "11 a.m." in row.text, "Los datos de hora no coinciden"

        except TimeoutException:
            self.fail("Franja horaria no encontrada después de la edición")
        
  
    
    
    def test3_eliminar_franja_horaria(self):
        """Prueba eliminar una Franja Horaria"""
        driver = self.driver
        driver.get("http://127.0.0.1:8000/api/horarios/list/")
        
        # Cambiar al tab Franjas Horarias
        driver.find_element(By.XPATH, "//a[@href='#timeslots']").click()
        time.sleep(2)
        
        driver.find_element(By.CLASS_NAME, "delete-btn").click()
        
        # Confirmar eliminación y hacer clic en OK
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()
        
        driver.refresh()
        time.sleep(2)
        
        self.assertFalse("09:00AM" in driver.page_source)
    

    
    def tearDown(self):
        self.driver.quit()