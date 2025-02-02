import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from unittest import TestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class VentanillaUITests(TestCase):
    def setUp(self):
        """Configuración inicial antes de cada prueba"""
        self.service = Service(
            "chromedriver/mac_arm-132.0.6834.110/chromedriver-mac-arm64/chromedriver"
        )
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.implicitly_wait(10)
        self.login()
        
    def login(self):
        """Helper method para hacer login antes de las pruebas"""
        self.driver.get("http://127.0.0.1:8000/")
        username_field = self.driver.find_element(By.NAME, "login")
        password_field = self.driver.find_element(By.NAME, "password")
        username_field.send_keys("test_user")
        password_field.send_keys("Yuy1t01506$")
        password_field.send_keys(Keys.RETURN)

        # Esperar a que aparezca un elemento que indique login exitoso
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ri-logout-box-line"))
        )

        # Navegar a la página de ventanillas
        self.driver.get("http://127.0.0.1:8000/api/core/ventanillas/")

    def test_1_crear_ventanilla(self):
        """
        Prueba la creación de una nueva ventanilla de prueba.
        """
        try:
            # Hacer clic en "Agregar Ventanilla"
            add_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "add-btn"))
            )
            add_button.click()

            # Esperar a que aparezca el modal y esté visible
            modal = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "showModal"))
            )
            
            # Esperamos un momento para que el modal se abra completamente
            time.sleep(0.5)
            
            # Verificar que el modal está visible
            self.assertTrue(modal.is_displayed(), "El modal no está visible")

            # Llenar el formulario con datos de la ventanilla de prueba
            self.driver.find_element(By.ID, "id_ventanilla").send_keys("101")
            self.driver.find_element(By.ID, "descripcion").send_keys("Ventanilla de Prueba")
            
            # Activar el switch de estado
            estado_switch = self.driver.find_element(By.ID, "estado")
            if not estado_switch.is_selected():
                estado_switch.click()

            # Hacer clic en el botón de guardar
            submit_button = self.driver.find_element(By.ID, "guardar-ventanilla-btn")
            submit_button.click()

            # Esperar a que aparezca el SweetAlert de éxito
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
            )

            # Hacer clic en el botón OK del SweetAlert
            ok_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
            )
            ok_button.click()

            # Esperar a que la tabla se actualice
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ventanillasTable"))
            )

            # Verificar que la ventanilla aparece en la tabla
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Ventanilla de Prueba')]"))
            )

            # Verificar que seguimos en la página correcta
            self.assertTrue(
                "api/core/ventanillas" in self.driver.current_url,
                "No estamos en la página correcta después de crear la ventanilla"
            )

        except TimeoutException as e:
            self.fail(f"Error al crear la ventanilla de prueba: {str(e)}")
        except Exception as e:
            self.fail(f"Error inesperado al crear la ventanilla: {str(e)}")


    
    def test_2_editar_ventanilla(self):
        """
        Prueba la edición de la ventanilla de prueba.
        """
        try:
            # Buscar la fila que contenga "Ventanilla de Prueba"
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ventanillasTable"))
            )
            
            fila_ventanilla = None
            rows = self.driver.find_elements(By.CSS_SELECTOR, "#ventanillasTable tbody tr")
            for row in rows:
                if "Ventanilla de Prueba" in row.text:
                    fila_ventanilla = row
                    break

            self.assertIsNotNone(fila_ventanilla, "No se encontró la ventanilla de prueba en la tabla.")

            # Hacer clic en el botón editar dentro de esa fila
            edit_button = fila_ventanilla.find_element(By.CLASS_NAME, "edit-btn")
            edit_button.click()

            # Esperar que aparezca el modal
            modal = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "showModal"))
            )

            # Esperar un momento para que el modal se abra completamente
            time.sleep(0.5)

            # Editar la descripción
            descripcion_field = self.driver.find_element(By.ID, "descripcion")
            descripcion_field.clear()
            descripcion_field.send_keys("Ventanilla de Prueba Editada")

            # Hacer clic en el botón de guardar usando el ID específico
            submit_button = self.driver.find_element(By.ID, "guardar-ventanilla-btn")
            submit_button.click()

            # Esperar mensaje de éxito
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
            )

            # Hacer clic en el botón OK del SweetAlert
            ok_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
            )
            ok_button.click()

            # Esperar a que la tabla se actualice
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ventanillasTable"))
            )

            # Verificar que la ventanilla se actualizó correctamente
            ventanilla_actualizada = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//td[contains(text(), 'Ventanilla de Prueba Editada')]")
                )
            )
            self.assertIsNotNone(ventanilla_actualizada, "La ventanilla no se editó correctamente.")

        except TimeoutException as e:
            self.fail(f"Error al editar la ventanilla de prueba: {str(e)}")
        except Exception as e:
            self.fail(f"Error inesperado al editar la ventanilla: {str(e)}")


    
    def test_3_eliminar_ventanilla(self):
        """
        Prueba la eliminación de la ventanilla de prueba.
        """
        try:
            # Buscar la fila que contenga "Ventanilla de Prueba Editada"
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ventanillasTable"))
            )
            
            fila_ventanilla = None
            rows = self.driver.find_elements(By.CSS_SELECTOR, "#ventanillasTable tbody tr")
            for row in rows:
                if "Ventanilla de Prueba Editada" in row.text:
                    fila_ventanilla = row
                    break

            self.assertIsNotNone(fila_ventanilla, "No se encontró la ventanilla de prueba en la tabla para eliminar.")

            # Hacer clic en el botón eliminar dentro de esa fila
            delete_button = fila_ventanilla.find_element(By.ID, f"delete-ventanilla-{fila_ventanilla.find_element(By.CLASS_NAME, 'id').text}")
            delete_button.click()

            # Confirmar eliminación en SweetAlert
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".swal2-confirm"))
            )
            confirm_button.click()

            # Esperar mensaje de éxito
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
            )

            # Verificar que la ventanilla se eliminó
            self.driver.refresh()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ventanillasTable"))
            )
            ventanillas_restantes = self.driver.find_elements(
                By.XPATH, "//td[contains(text(), 'Ventanilla de Prueba Editada')]"
            )
            self.assertTrue(len(ventanillas_restantes) == 0, "La ventanilla no se eliminó correctamente.")

        except TimeoutException as e:
            self.fail(f"Error al eliminar la ventanilla de prueba: {str(e)}")

    def tearDown(self):
        """Cerrar el navegador después de cada prueba"""
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()