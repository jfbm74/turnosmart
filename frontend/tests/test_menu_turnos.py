import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class MenuTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuración que se ejecuta una vez antes de todas las pruebas"""
        cls.base_url = "http://127.0.0.1:8000"
        cls.test_user = "test_user"
        cls.test_password = "Yuy1t01506$"

    def setUp(self):
        """Configuración que se ejecuta antes de cada prueba"""
        self.service = Service("chromedriver/mac_arm-132.0.6834.110/chromedriver-mac-arm64/chromedriver")
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        self.login()
        
    def login(self):
        """Helper method para hacer login"""
        self.driver.get(self.base_url)
        username_field = self.driver.find_element(By.NAME, "login")
        password_field = self.driver.find_element(By.NAME, "password")
        username_field.send_keys(self.test_user)
        password_field.send_keys(self.test_password)
        password_field.send_keys(Keys.RETURN)
        
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "ri-logout-box-line"))
        )
        
        self.driver.get(f"{self.base_url}/api/menu/list/")
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "add-btn"))
        )

    def agregar_menu_helper(self, nombre, tipo, horario_general, descripcion):
        """Helper method para agregar un menú"""
        driver = self.driver
        
        # Abrir modal
        driver.find_element(By.CLASS_NAME, "add-btn").click()
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "showModal"))
        )
        
        # Llenar formulario
        driver.find_element(By.ID, "nombre").send_keys(nombre)
        Select(driver.find_element(By.ID, "tipo")).select_by_value(tipo)
        Select(driver.find_element(By.ID, "horario_general")).select_by_value(str(horario_general))
        
        # Seleccionar prioridad/trámite según el tipo
        if tipo == "CONTENEDOR":
            try:
                prioridad_select = Select(driver.find_element(By.ID, "prioridad"))
                if len(prioridad_select.options) > 1:
                    prioridad_select.select_by_index(1)
            except NoSuchElementException:
                pass
        elif tipo == "TRAMITE":
            try:
                tramite_select = Select(driver.find_element(By.ID, "tramite"))
                if len(tramite_select.options) > 1:
                    tramite_select.select_by_index(1)
            except NoSuchElementException:
                pass
        
        driver.find_element(By.ID, "descripcion").send_keys(descripcion)
        
        # Guardar y confirmar
        self.wait.until(
            EC.element_to_be_clickable((By.ID, "boton-guardar"))
        ).click()
        
        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()
        
        # Verificar creación
        driver.refresh()
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{nombre}')]"))
        )
        
        return nombre

    def test_01_agregar_menu_contenedor(self):
        """Prueba agregar un nuevo Menú tipo Contenedor"""
        nombre = "Menú Contenedor Test"
        self.agregar_menu_helper(
            nombre=nombre,
            tipo="CONTENEDOR",
            horario_general=True,
            descripcion="Descripción del menú contenedor de prueba"
        )
        self.assertTrue(nombre in self.driver.page_source)

    def test_02_agregar_menu_tramite(self):
        """Prueba agregar un nuevo Menú tipo Trámite"""
        nombre = "Menú Trámite Test"
        self.agregar_menu_helper(
            nombre=nombre,
            tipo="TRAMITE",
            horario_general=False,
            descripcion="Descripción del menú trámite de prueba"
        )
        self.assertTrue(nombre in self.driver.page_source)

    def test_03_editar_menu(self):
        """Prueba editar un Menú existente"""
        driver = self.driver
        nuevo_nombre = "Menú Editado Test"
        
        # Hacer clic en editar
        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "edit-btn"))
        ).click()
        
        # Editar campos
        nombre_input = self.wait.until(
            EC.visibility_of_element_located((By.ID, "nombre"))
        )
        nombre_input.clear()
        nombre_input.send_keys(nuevo_nombre)
        
        descripcion_input = driver.find_element(By.ID, "descripcion")
        descripcion_input.clear()
        descripcion_input.send_keys("Nueva descripción del menú editado")
        
        # Guardar cambios
        self.wait.until(
            EC.element_to_be_clickable((By.ID, "boton-guardar"))
        ).click()
        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()
        
        # Verificar cambios
        driver.refresh()
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{nuevo_nombre}')]"))
        )
        self.assertTrue(nuevo_nombre in driver.page_source)

    def test_04_buscar_menu(self):
        """Prueba la funcionalidad de búsqueda"""
        driver = self.driver
        nombre_busqueda = "Menú Editado Test"
        
        # Realizar búsqueda
        search_input = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "search"))
        )
        search_input.clear()
        search_input.send_keys(nombre_busqueda)
        search_input.send_keys(Keys.RETURN)  # Presionar Enter para activar la búsqueda
        
        # Esperar a que los resultados se actualicen
        time.sleep(1)
        
        # Verificar resultados
        results = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, f"//td[contains(text(), '{nombre_busqueda}')]"))
        )
        self.assertGreater(len(results), 0, "No se encontraron resultados en la búsqueda")

    def test_05_validar_formulario(self):
        """Prueba las validaciones del formulario"""
        driver = self.driver
        
        # Abrir formulario vacío
        driver.find_element(By.CLASS_NAME, "add-btn").click()
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "showModal"))
        )
        
        # Intentar guardar sin datos
        self.wait.until(
            EC.element_to_be_clickable((By.ID, "boton-guardar"))
        ).click()
        
        # Verificar que el modal sigue visible
        self.assertTrue(
            driver.find_element(By.ID, "showModal").is_displayed(),
            "El formulario se envió sin datos requeridos"
        )
        
        # Verificar mensaje de validación
        nombre_input = driver.find_element(By.ID, "nombre")
        validation_message = nombre_input.get_attribute("validationMessage")
        self.assertIn(
            validation_message,
            ["Please fill out this field.", "Completa este campo"],
            "No se mostró un mensaje de validación válido"
        )

    def test_06_eliminar_menu(self):
        """Prueba eliminar un Menú"""
        driver = self.driver
        nombre_menu = "Menú Editado Test"
        
        # Esperar y hacer clic en el botón eliminar
        delete_btn = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "delete-btn"))
        )
        driver.execute_script("arguments[0].click();", delete_btn)
        
        # Esperar y confirmar el primer diálogo
        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
        ).click()
        
        # Esperar y confirmar el segundo diálogo
        try:
            self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
            ).click()
        except:
            pass  # Ignorar si no aparece el segundo diálogo
        
        # Verificar eliminación
        driver.refresh()
        time.sleep(1)  # Pequeña espera para asegurar que la página se recargó
        
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{nombre_menu}')]"))
            )
            self.fail("El menú no fue eliminado correctamente")
        except TimeoutException:
            pass  # La prueba pasa si el elemento no se encuentra

    def tearDown(self):
        """Limpieza después de cada prueba"""
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()