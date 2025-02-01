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

class VideoConfigurationTests(TestCase):
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

    def navigate_to_videos(self):
        """Helper method para navegar a la página de videos"""
        self.driver.get("http://127.0.0.1:8000/api/configuracion/videos/")
        # Esperar por el ID de la tabla en lugar de la clase
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "institucionesTable"))
        )

    def test_1_crear_video(self):
        """Prueba la creación exitosa de un video"""
        self.navigate_to_videos()
        
        try:
            # Esperar por el botón de agregar y hacer clic
            add_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "add-btn"))
            )
            add_button.click()
            
            # Esperar que el modal se abra
            modal = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "showModal"))
            )
            
            # Llenar el formulario
            nombre_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "nombre"))
            )
            nombre_input.send_keys("Video Test")
            
            self.driver.find_element(By.ID, "origen").send_keys("URL")
            self.driver.find_element(By.ID, "url_video").send_keys("http://example.com/video.mp4")
            self.driver.find_element(By.ID, "estado").send_keys("True")
            
            # Enviar formulario
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#videoForm button[type='submit']"))
            )
            submit_button.click()
            
            # Verificar mensaje de éxito
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
            )
            
        except TimeoutException as e:
            self.fail(f"No se pudo completar la creación del video: {str(e)}")

    def test_2_campos_requeridos_video(self):
        """Prueba la validación de campos requeridos al crear un video"""
        self.navigate_to_videos()
        
        try:
            # Abrir modal de creación
            add_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "add-btn"))
            )
            add_button.click()
            
            # Esperar que el modal se abra
            modal = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "showModal"))
            )
            
            # Intentar enviar el formulario sin llenar campos
            submit_button = modal.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            # Verificar que el modal sigue abierto
            time.sleep(1)
            self.assertTrue(modal.is_displayed(), "El modal debería permanecer abierto si hay errores de validación")
            
        except TimeoutException as e:
            self.fail(f"Error en la prueba de campos requeridos: {str(e)}")

    def test_3_editar_video(self):
        """Prueba la edición de un video existente"""
        self.navigate_to_videos()
        
        try:
            # Esperar a que la tabla esté cargada
            table = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "institucionesTable"))
            )
            
            # Buscar el primer botón de editar por su ID parcial
            edit_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[id^='editBtn-']"))
            )

            # Hacer clic en el botón usando JavaScript
            self.driver.execute_script("arguments[0].click();", edit_button)
            
            # Esperar a que el modal se abra Y el título sea correcto
            def check_modal_title(driver):
                try:
                    modal = driver.find_element(By.ID, "showModal")
                    title = driver.find_element(By.ID, "exampleModalLabel")
                    return modal.is_displayed() and title.text == "Editar Video"
                except:
                    return False

            # Esperar hasta que el modal esté abierto y el título sea correcto
            WebDriverWait(self.driver, 10).until(check_modal_title)
            
            # Verificar que podemos interactuar con el formulario
            nombre_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "nombre"))
            )
            nombre_input.clear()
            nombre_input.send_keys("Video Actualizado Test")
            
            # Guardar cambios
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#videoForm button[type='submit']"))
            )
            submit_button.click()
            
            # Verificar mensaje de éxito
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
            )
            
        except TimeoutException as e:
            self.fail(f"Error de timeout: {str(e)}\nEs posible que el modal no se haya abierto o que el título no se haya actualizado correctamente.")
        except Exception as e:
            self.fail(f"Error inesperado: {str(e)}")

    def test_4_busqueda_video(self):
        """Prueba la funcionalidad de búsqueda de videos"""
        self.navigate_to_videos()
        
        try:
            # Realizar búsqueda
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "search"))
            )
            search_input.clear()
            search_input.send_keys("test")
            time.sleep(2)
            
            # Verificar resultados en la tabla
            table = self.driver.find_element(By.ID, "institucionesTable")
            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
            
            found_match = False
            for row in rows:
                if "test" in row.text.lower():
                    found_match = True
                    break
            
            self.assertTrue(found_match, "No se encontró ningún video con 'test' en el nombre")
            
        except TimeoutException as e:
            self.fail(f"Error en la búsqueda: {str(e)}")

    def test_5_eliminar_videos_prueba(self):
        """Prueba la eliminación de videos"""
        self.navigate_to_videos()

        nombres_a_eliminar = ["Video Test", "Video Actualizado Test"]

        for nombre in nombres_a_eliminar:
            while True:
                try:
                    # Buscar el video
                    search_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "search"))
                    )
                    search_input.clear()
                    search_input.send_keys(nombre)
                    time.sleep(2)

                    # Buscar en la tabla
                    table = self.driver.find_element(By.ID, "institucionesTable")
                    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

                    if not rows:
                        break

                    for row in rows:
                        nombre_celda = row.find_elements(By.TAG_NAME, "td")[1].text.strip()
                        if nombre_celda == nombre:
                            # Encontrar y hacer clic en el botón de eliminar
                            delete_button = row.find_element(By.CSS_SELECTOR, "button.btn-soft-danger")
                            self.driver.execute_script("arguments[0].click();", delete_button)

                            # Confirmar eliminación
                            confirm_button = WebDriverWait(self.driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, ".swal2-confirm"))
                            )
                            confirm_button.click()

                            # Esperar mensaje de éxito
                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
                            )
                            
                            time.sleep(2)
                            self.driver.refresh()
                            break
                    else:
                        break

                except TimeoutException:
                    break

        # Verificación final
        for nombre in nombres_a_eliminar:
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "search"))
            )
            search_input.clear()
            search_input.send_keys(nombre)
            time.sleep(2)

            table = self.driver.find_element(By.ID, "institucionesTable")
            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
            for row in rows:
                nombre_celda = row.find_elements(By.TAG_NAME, "td")[1].text.strip()
                self.assertNotEqual(nombre_celda, nombre, 
                    f"El video '{nombre}' aún existe después de ser eliminado")

    def tearDown(self):
        """Limpieza después de cada prueba"""
        if self.driver:
            self.driver.quit()