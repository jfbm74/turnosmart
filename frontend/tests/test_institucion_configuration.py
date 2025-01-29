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

class InstitucionConfigurationTests(TestCase):
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

    def navigate_to_institucion(self):
        """Helper method para navegar a la página de instituciones"""
        self.driver.get("http://127.0.0.1:8000/api/configuracion/instituciones/")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "listjs-table"))
        )

    def test_1_crear_institucion(self):
        """Prueba la creación exitosa de una institución"""
        self.navigate_to_institucion()
        
        # Abrir modal de creación
        self.driver.find_element(By.CLASS_NAME, "add-btn").click()
        
        # Esperar que el modal se abra
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "showModal"))
        )
        
        # Llenar el formulario
        self.driver.find_element(By.ID, "nombre").send_keys("Institución Test")
        self.driver.find_element(By.ID, "siglas").send_keys("TEST")
        self.driver.find_element(By.ID, "direccion").send_keys("Dirección Test")
        self.driver.find_element(By.ID, "telefono").send_keys("123456789")
        self.driver.find_element(By.ID, "email").send_keys("test@test.com")
        
        # Enviar formulario
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "#institucionForm button[type='submit']")
        submit_button.click()
        
        # Verificar mensaje de éxito
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
            )
        except TimeoutException:
            self.fail("No se mostró el mensaje de éxito")

    def test_2_campos_requeridos_institucion(self):
        """Prueba la validación de campos requeridos al crear una institución"""
        self.navigate_to_institucion()
        
        # Abrir modal de creación
        self.driver.find_element(By.CLASS_NAME, "add-btn").click()
        
        # Esperar que el modal se abra
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "showModal"))
        )
        
        # Intentar enviar el formulario sin llenar campos
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "#institucionForm button[type='submit']")
        submit_button.click()
        
        # Verificar que el formulario no se envió (el modal sigue abierto)
        try:
            modal = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.ID, "showModal"))
            )
            self.assertTrue(modal.is_displayed(), "El modal debería permanecer abierto si hay errores de validación")
        except TimeoutException:
            self.fail("El modal se cerró a pesar de tener campos requeridos vacíos")

    def test_4_busqueda_institucion(self):
        """Prueba la funcionalidad de búsqueda de instituciones"""
        self.navigate_to_institucion()
        
        # Realizar búsqueda
        search_input = self.driver.find_element(By.CLASS_NAME, "search")
        search_input.clear()
        search_input.send_keys("test")
        
        # Dar tiempo para que se aplique el filtro (considerando el debounce de 300ms)
        time.sleep(1)
        
        # Verificar resultados
        try:
            # Esperar a que la búsqueda se complete
            WebDriverWait(self.driver, 5).until(
                lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "tbody.list tr")) > 0
            )
            
            # Verificar resultados
            rows = self.driver.find_elements(By.CSS_SELECTOR, "tbody.list tr")
            found_match = False
            for row in rows:
                if "no se encontraron resultados" in row.text.lower():
                    continue
                nombre_td = row.find_element(By.CLASS_NAME, "nombre")
                if "test" in nombre_td.text.lower():
                    found_match = True
                    break
            
            self.assertTrue(found_match, "No se encontró ninguna institución con 'test' en el nombre")
        except TimeoutException:
            self.fail("La búsqueda no produjo resultados en el tiempo esperado")

    
    def test_3_editar_institucion(self):
        """Prueba la edición de una institución existente"""
        self.navigate_to_institucion()
        
        try:
            # Esperar y encontrar el botón de editar
            edit_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.edit-btn"))
            )
            
            # Click en el botón de editar
            self.driver.execute_script("arguments[0].click();", edit_button)
            
            # Esperar que el modal se abra
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "showModal"))
            )

            # Verificar que el título del modal cambió
            modal_title = self.driver.find_element(By.ID, "exampleModalLabel")
            self.assertEqual(modal_title.text, "Editar Institución")
            
            # Modificar campos
            nombre_input = self.driver.find_element(By.ID, "nombre")
            nombre_input.clear()
            nombre_input.send_keys("Institución Actualizada Test")
            
            # Guardar cambios
            submit_button = self.driver.find_element(By.ID, "btnGuardarCambios")
            submit_button.click()
            
            # Verificar mensaje de éxito
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
            )

            # Verificar que la tabla se actualizó (opcional)
            self.driver.refresh()  # Recargar la página
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "listjs-table"))
            )
            
            # Buscar el texto actualizado
            updated_cells = self.driver.find_elements(By.CLASS_NAME, "nombre")
            found_updated = any("Institución Actualizada Test" in cell.text for cell in updated_cells)
            self.assertTrue(found_updated, "No se encontró la institución actualizada en la tabla")

        except TimeoutException as e:
            self.fail(f"No se pudo completar la edición de la institución: {str(e)}")
        except Exception as e:
            self.fail(f"Error durante la prueba de edición: {str(e)}")

    
    def test_5_eliminar_institucion(self):
        """Prueba la eliminación de una institución existente"""
        self.navigate_to_institucion()
        
        try:
            # Esperar y encontrar el botón de eliminar
            delete_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.delete-btn"))
            )
            
            # Obtener el nombre de la institución antes de eliminar (para verificación)
            institucion_nombre = delete_button.get_attribute('data-nombre')
            institucion_id = delete_button.get_attribute('data-id')
            
            # Click en el botón de eliminar
            self.driver.execute_script("arguments[0].click();", delete_button)
            
            # Esperar que aparezca el diálogo de confirmación de SweetAlert2
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-popup"))
            )
            
            # Verificar el mensaje de confirmación
            confirmation_message = self.driver.find_element(
                By.CLASS_NAME, "swal2-html-container"
            ).text
            expected_message = f'¿Deseas eliminar la institución "{institucion_nombre}"?'
            self.assertEqual(confirmation_message, expected_message)
            
            # Click en el botón "Sí, eliminar"
            confirm_button = self.driver.find_element(
                By.CSS_SELECTOR, ".swal2-confirm"
            )
            confirm_button.click()
            
            # Esperar el mensaje de éxito
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
            )
            
            # Esperar a que se recargue la página
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "listjs-table"))
            )
            
            # Verificar que la institución ya no existe en la tabla
            try:
                # Intentar buscar el registro eliminado
                self.driver.find_element(
                    By.CSS_SELECTOR, f"button[data-id='{institucion_id}']"
                )
                self.fail("La institución aún existe en la tabla después de ser eliminada")
            except:
                # Si no se encuentra el elemento, la prueba es exitosa
                pass

        except TimeoutException as e:
            self.fail(f"No se pudo completar la eliminación de la institución: {str(e)}")
        except Exception as e:
            self.fail(f"Error durante la prueba de eliminación: {str(e)}")



    def tearDown(self):
        """Limpieza después de cada prueba"""
        if self.driver:
            self.driver.quit()