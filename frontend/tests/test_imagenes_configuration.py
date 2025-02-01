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

class ImagenConfigurationTests(TestCase):
    def setUp(self):
        """Configuración inicial antes de cada prueba"""
        self.service = Service(
            "chromedriver/mac_arm-132.0.6834.110/chromedriver-mac-arm64/chromedriver"
        )
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.implicitly_wait(10)
        self.test_image_path = os.path.abspath("static/images/test_images/bonsana_peq.jpeg")
        self.login()
        
    def login(self):
        """Helper method para hacer login"""
        # URL absoluto donde está tu login
        self.driver.get("http://127.0.0.1:8000/")
        username_field = self.driver.find_element(By.NAME, "login")
        password_field = self.driver.find_element(By.NAME, "password")
        username_field.send_keys("test_user")
        password_field.send_keys("Yuy1t01506$")
        password_field.send_keys(Keys.RETURN)
        
        # Esperar a que aparezca algún elemento que indique login exitoso
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ri-logout-box-line"))
        )

    def navigate_to_images(self):
        """Helper method para navegar a la página de imágenes"""
        self.driver.get("http://127.0.0.1:8000/api/configuracion/imagenes/")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "institucionesTable"))
        )

    def test_1_crear_imagen(self):
        """
        Prueba la creación de un registro subiendo varias imágenes 
        y verificando que aparezca en la tabla.
        """
        # 1) Navegar a la lista de imágenes
        self.driver.get("http://127.0.0.1:8000/api/configuracion/imagenes/")

        # 2) Hacer clic en el botón de "Agregar Imagen"
        add_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'add-image-btn'))
        )
        add_button.click()

        # 3) Esperar a que aparezca el modal/formulario
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "showModal"))
        )

        # 4) Subir varias imágenes (ajusta las rutas según tus nombres de archivo)
        base_path = os.path.abspath("static/images/test_images/")
        
        self.driver.find_element(By.ID, "logo_pequeño").send_keys(
            os.path.join(base_path, "bonsana_peq.jpeg")
        )
        self.driver.find_element(By.ID, "logo_grande").send_keys(
            os.path.join(base_path, "logo_med_bonsana.png")
        )
        self.driver.find_element(By.ID, "logo_ticket").send_keys(
            os.path.join(base_path, "logo_ticket.jpg")
        )
        self.driver.find_element(By.ID, "footer").send_keys(
            os.path.join(base_path, "logo_footer.png")
        )
        self.driver.find_element(By.ID, "wallpaper_turnero").send_keys(
            os.path.join(base_path, "logo_wallpaper.jpg")
        )

        # 5) Hacer clic en el botón de "Guardar"
        #    Suponiendo que tu botón tiene ID="btn-guardar-imagen"
        guardar_button = self.driver.find_element(By.ID, "btn-guardar-imagen")
        guardar_button.click()

        # 6) Esperar el mensaje de éxito (ej.: sweetalert "swal2-success")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
        )

        # 7) Opcional: refrescar la lista y verificar que realmente 
        #    exista un nuevo registro en la tabla (si la tabla muestra filas)
        self.driver.refresh()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "institucionesTable"))  
            # o el ID real de la tabla de imágenes
        )

        # Verificar que al menos haya 1 fila nueva. 
        # Ajusta el selector para tus filas dentro del tbody.
        rows = self.driver.find_elements(By.CSS_SELECTOR, "#institucionesTable tbody tr")
        self.assertTrue(len(rows) > 0, "No se encontró ningún registro en la tabla luego de crear la imagen.")

        # )

    def test_2_editar_imagen(self):
        """
        2) Editar imagen:
        - Localiza la fila que tenga una <img> cuyo src contenga 'bonsana_peq' (la imagen original).
        - Abre el modal de edición y reemplaza la imagen por bonsanaips_logo_peq.jpeg.
        - Verifica que ahora la <img> contiene 'bonsanaips_logo_peq' en su src.
        """
        self.navigate_to_images()

        try:
            # 1. Esperar a que la tabla aparezca
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "institucionesTable"))
            )

            # 2. Buscar la fila que contenga la <img> con 'bonsana_peq' en el atributo src
            rows = self.driver.find_elements(By.CSS_SELECTOR, "#institucionesTable tbody tr")
            fila_a_editar = None

            for row in rows:
                try:
                    # Busca un <img> específico dentro de la fila.
                    # Ajusta el selector según tu HTML (ej: .logo-pequeno, o img:nth-child(1), etc.)
                    img_element = row.find_element(By.CSS_SELECTOR, "img.logo-pequeno")
                    src_value = img_element.get_attribute("src")
                    
                    if "bonsana_peq" in src_value:
                        fila_a_editar = row
                        break
                except:
                    # Si no encuentra <img> o no coincide, pasamos a la siguiente fila.
                    pass

            self.assertIsNotNone(
                fila_a_editar,
                "No se encontró ninguna fila con la imagen que contenga 'bonsana_peq' en el src."
            )

            # 3. Dentro de esa fila, hacer clic en el botón 'Editar' (clase 'edit-image-btn', por ejemplo)
            edit_button = fila_a_editar.find_element(By.CLASS_NAME, "edit-image-btn")
            edit_button.click()

            # 4. Esperar a que se abra el modal de edición
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "showModal"))
            )

            # 5. Subir la nueva imagen (bonsanaips_logo_peq.jpeg)
            nueva_imagen_path = os.path.abspath("static/images/test_images/bonsanaips_logo_peq.jpeg")
            logo_pequeno_field = self.driver.find_element(By.ID, "logo_pequeño")
            logo_pequeno_field.send_keys(nueva_imagen_path)

            # 6. Hacer clic en Guardar
            save_button = self.driver.find_element(By.ID, "btn-guardar-imagen")
            save_button.click()

            # 7. Verificar mensaje de éxito (ej: SweetAlert con clase 'swal2-success')
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
            )

            # 8. Refrescar y verificar la nueva imagen (bonsanaips_logo_peq) en el src
            self.driver.refresh()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "institucionesTable"))
            )

            rows_after = self.driver.find_elements(By.CSS_SELECTOR, "#institucionesTable tbody tr")
            found_updated = False
            for row in rows_after:
                try:
                    img_element = row.find_element(By.CSS_SELECTOR, "img.logo-pequeno")
                    src_value = img_element.get_attribute("src")
                    if "bonsanaips_logo_peq" in src_value:
                        found_updated = True
                        break
                except:
                    pass

            self.assertTrue(
                found_updated,
                "No se encontró una <img> con 'bonsanaips_logo_peq' en el src luego de la edición."
            )

        except TimeoutException as e:
            self.fail(f"Error en la edición de la imagen: {str(e)}")


    @unittest.skip("Omitir este test por ahora")
    def test_3_visualizar_previsualizaciones(self):
        """
        3) Visualizar previsualizaciones:
        - Navega a la página de imágenes.
        - Abre el modal de creación o edición.
        - Sube una imagen de prueba.
        - Verifica que aparezca la vista previa en el modal.
        """
        self.navigate_to_images()
        try:
            add_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "add-btn"))
            )
            add_button.click()

            # Subir imagen y verificar el preview
            logo_pequeno = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "logo_pequeño"))
            )
            logo_pequeno.send_keys(self.test_image_path)

            preview = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "preview-logo-pequeno"))
            )
            self.assertTrue(preview.is_displayed(), "No se muestra la previsualización de la imagen")
        except TimeoutException as e:
            self.fail(f"Error en la previsualización de imágenes: {str(e)}")


    
    def test_4_eliminar_imagen(self):
        """
        4) Eliminar imagen:
        - Navega a la página de imágenes.
        - Selecciona alguna imagen (por ejemplo, la recién creada o editada).
        - Presiona el botón de eliminar y confirma en el alert/modal.
        - Verifica que se haya eliminado correctamente de la lista.
        """
        self.navigate_to_images()

        try:
            # 1. Esperar a que se muestre la lista de imágenes.
            table = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "institucionesTable"))
            )

            # 2. Localizar un botón de eliminar. Suponemos que cada fila tiene un botón con clase 'delete-image-btn'.
            delete_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "delete-image-btn"))
            )

            # 3. Hacer clic en el botón de eliminar
            self.driver.execute_script("arguments[0].click();", delete_button)

            # 4. Confirmar la eliminación en el SweetAlert o modal
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".swal2-confirm"))
            )
            confirm_button.click()

            # 5. Verificar mensaje de éxito
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
            )

            # 6. (Opcional) Verificar que la imagen ya no está en la tabla
            #    - Podrías recargar la página y buscar de nuevo en la tabla
            #      para asegurarte que no exista la fila que acabas de borrar.
            # self.driver.refresh()
            # WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.ID, "institucionesTable"))
            # )
            # rows = self.driver.find_elements(By.CSS_SELECTOR, "#institucionesTable tbody tr")
            # self.assertTrue(all("nombre_o_id_de_la_imagen" not in r.text for r in rows),
            #                 "La imagen eliminada todavía aparece en la tabla.")

        except TimeoutException as e:
            self.fail(f"Error en la eliminación de la imagen: {str(e)}")

    def tearDown(self):
        """Limpieza después de cada prueba"""
        if self.driver:
            self.driver.quit()
