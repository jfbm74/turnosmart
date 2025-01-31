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

class TicketConfigurationTests(TestCase):
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

    def navigate_to_ticket_configuration(self):
        """Helper method para navegar a la página de configuración de tickets"""
        self.driver.get("http://127.0.0.1:8000/api/configuracion/tickets/")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "listjs-table"))
        )

    def test_1_crear_configuracion_ticket(self):
        """Prueba la creación exitosa de una configuración de ticket"""
        self.navigate_to_ticket_configuration()
        
        # Abrir modal de creación
        self.driver.find_element(By.CLASS_NAME, "add-btn").click()
        
        # Esperar que el modal se abra
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "showModal"))
        )
        
        # Llenar el formulario
        self.driver.find_element(By.ID, "nombre").send_keys("Configuración Test")
        self.driver.find_element(By.ID, "ancho_ticket").send_keys("80")
        
        # Configuraciones adicionales
        logo_visible_checkbox = self.driver.find_element(By.ID, "logo_visible")
        if not logo_visible_checkbox.is_selected():
            logo_visible_checkbox.click()
        
        tramite_visible_checkbox = self.driver.find_element(By.ID, "tramite_visible")
        if not tramite_visible_checkbox.is_selected():
            tramite_visible_checkbox.click()
        
        # Llenar algunos campos de fuente
        self.driver.find_element(By.ID, "fuente_turno").send_keys("12")
        self.driver.find_element(By.ID, "fuente_tramite").send_keys("10")
        
        # Enviar formulario
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "#ticketForm button[type='submit']")
        submit_button.click()
        
        # Verificar mensaje de éxito
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
            )
        except TimeoutException:
            self.fail("No se mostró el mensaje de éxito")

    def test_2_campos_requeridos_ticket(self):
        """Prueba la validación de campos requeridos al crear una configuración de ticket"""
        self.navigate_to_ticket_configuration()
        
        # Abrir modal de creación
        self.driver.find_element(By.CLASS_NAME, "add-btn").click()
        
        # Esperar que el modal se abra
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "showModal"))
        )
        
        # Intentar enviar el formulario sin llenar campos
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "#ticketForm button[type='submit']")
        submit_button.click()
        
        # Verificar que el formulario no se envió (el modal sigue abierto)
        try:
            modal = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.ID, "showModal"))
            )
            self.assertTrue(modal.is_displayed(), "El modal debería permanecer abierto si hay errores de validación")
        except TimeoutException:
            self.fail("El modal se cerró a pesar de tener campos requeridos vacíos")

    def test_3_editar_configuracion_ticket(self):
        """Prueba la edición de una configuración de ticket existente"""
        self.navigate_to_ticket_configuration()
        
        try:
            # Esperar y encontrar el botón de editar con el selector correcto
            edit_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.btn-sm.btn-soft-primary")
            
            # Verificar que hay al menos un botón de edición
            self.assertTrue(len(edit_buttons) > 0, "No hay configuraciones de ticket para editar")
            
            # Click en el primer botón de editar
            edit_buttons[0].click()
            
            # Esperar que el modal se abra
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "showModal"))
            )

            # Verificar que el título del modal es exactamente "Editar Configuración de Ticket"
            modal_title = self.driver.find_element(By.ID, "exampleModalLabel")
            self.assertEqual(
                modal_title.text, 
                "Editar Configuración de Ticket", 
                f"Título del modal incorrecto. Encontrado: {modal_title.text}"
            )
            
            # Modificar campos
            nombre_input = self.driver.find_element(By.ID, "nombre")
            nombre_input.clear()
            nombre_input.send_keys("Configuración Actualizada Test")
            
            # Cambiar algunos valores
            ancho_ticket_input = self.driver.find_element(By.ID, "ancho_ticket")
            ancho_ticket_input.clear()
            ancho_ticket_input.send_keys("90")
            
            # Guardar cambios
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "#ticketForm button[type='submit']")
            submit_button.click()
            
            # Verificar mensaje de éxito
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
            )

            # Verificar que la tabla se actualizó
            self.driver.refresh()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "listjs-table"))
            )
            
            # Buscar el texto actualizado
            updated_cells = self.driver.find_elements(By.CLASS_NAME, "nombre")
            found_updated = any("Configuración Actualizada Test" in cell.text for cell in updated_cells)
            self.assertTrue(found_updated, "No se encontró la configuración de ticket actualizada en la tabla")

        except TimeoutException as e:
            self.fail(f"No se pudo completar la edición de la configuración de ticket: {str(e)}")
        except Exception as e:
            self.fail(f"Error durante la prueba de edición: {str(e)}")

    
    """
      def test_4_busqueda_configuracion_ticket(self): 
       
        self.navigate_to_ticket_configuration()
        
        # Primero, asegurarse de que hay datos para buscar
        self.create_test_ticket_if_not_exists()
        
        # Realizar búsqueda
        search_input = self.driver.find_element(By.CLASS_NAME, "search")
        search_input.clear()
        search_input.send_keys("Configuración")
        
        # Dar tiempo para que se aplique el filtro
        time.sleep(2)
        
        # Verificar resultados
        try:
            # Verificar resultados directamente sin espera de WebDriverWait
            rows = self.driver.find_elements(By.CSS_SELECTOR, "tbody.list tr")
            
            # Imprimir información de depuración
            print(f"Número de filas encontradas: {len(rows)}")
            for row in rows:
                print(f"Fila: {row.text}")
            
            # Verificar resultados
            found_match = False
            for row in rows:
                if "no se encontraron resultados" in row.text.lower():
                    continue
                nombre_td = row.find_element(By.CLASS_NAME, "nombre")
                if "configuración" in nombre_td.text.lower():
                    found_match = True
                    break
            
            self.assertTrue(found_match, "No se encontró ninguna configuración de ticket con 'Configuración' en el nombre")
        
        except Exception as e:
            # Imprimir información detallada del error
            print(f"Error en la búsqueda: {str(e)}")
            self.fail(f"Error durante la búsqueda: {str(e)}")
    """

    def create_test_ticket_if_not_exists(self):
        """Método auxiliar para crear un ticket de prueba si no existe"""
        try:
            # Navegar a la configuración de tickets
            self.navigate_to_ticket_configuration()
            
            # Verificar si hay tickets existentes
            rows = self.driver.find_elements(By.CSS_SELECTOR, "tbody.list tr")
            
            # Si no hay tickets, crear uno
            if not rows or len(rows) == 0:
                # Encontrar y hacer clic en el botón de agregar
                add_button = self.driver.find_element(By.CLASS_NAME, "add-btn")
                add_button.click()
                
                # Esperar a que se abra el modal
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "showModal"))
                )
                
                # Llenar los datos del ticket
                self.driver.find_element(By.ID, "nombre").send_keys("Configuración Test")
                self.driver.find_element(By.ID, "ancho_ticket").send_keys("80")
                
                # Enviar el formulario
                submit_button = self.driver.find_element(By.CSS_SELECTOR, "#ticketForm button[type='submit']")
                submit_button.click()
                
                # Esperar mensaje de éxito
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
                )
                
                # Refrescar la página
                self.driver.refresh()
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "listjs-table"))
                )
        except Exception as e:
            print(f"Error creando ticket de prueba: {str(e)}")
            raise



    def test_5_eliminar_configuraciones_ticket(self):
        """Prueba la eliminación de configuraciones de ticket"""
        self.navigate_to_ticket_configuration()

        nombres_a_eliminar = ["Configuración Test", "Configuración Actualizada Test"]

        for nombre in nombres_a_eliminar:
            while True:
                # Buscar la configuración en la tabla
                search_input = self.driver.find_element(By.CLASS_NAME, "search")
                search_input.clear()
                search_input.send_keys(nombre)
                time.sleep(2)  # Esperar a que se filtren los resultados

                rows = self.driver.find_elements(By.CSS_SELECTOR, "tbody.list tr:not(.no-result-message)")

                # Si no hay más resultados, terminamos la eliminación de este nombre
                if not rows:
                    break

                # Iterar sobre las filas para buscar coincidencias exactas
                found = False
                for row in rows:
                    try:
                        nombre_celda = row.find_element(By.CLASS_NAME, "nombre").text.strip()
                        if nombre_celda == nombre:
                            found = True
                            # Encontró la configuración, proceder con la eliminación
                            delete_button = row.find_element(By.CSS_SELECTOR, "button.btn-soft-danger")
                            self.driver.execute_script("arguments[0].click();", delete_button)

                            # Confirmar la eliminación en SweetAlert
                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "swal2-popup"))
                            )
                            confirm_button = self.driver.find_element(By.CSS_SELECTOR, ".swal2-confirm")
                            confirm_button.click()

                            # Esperar mensaje de éxito y que la tabla se recargue
                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
                            )
                            time.sleep(2)  # Dar tiempo para la actualización

                            # Recargar la página para verificar nuevamente
                            self.driver.refresh()
                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "listjs-table"))
                            )
                            break  # Salir del loop y volver a buscar desde el principio

                    except Exception as e:
                        print(f"Error al procesar fila: {e}")
                        continue

                if not found:
                    break  # Si no encontró coincidencias en la búsqueda, salir del loop

        # Verificación final: confirmar que no existen más configuraciones con esos nombres
        for nombre in nombres_a_eliminar:
            search_input = self.driver.find_element(By.CLASS_NAME, "search")
            search_input.clear()
            search_input.send_keys(nombre)
            time.sleep(2)

            rows = self.driver.find_elements(By.CSS_SELECTOR, "tbody.list tr:not(.no-result-message)")
            assert not rows, f"La configuración de ticket '{nombre}' aún existe en la tabla después de ser eliminada"

    def tearDown(self):
        """Limpieza después de cada prueba"""
        if self.driver:
            self.driver.quit()