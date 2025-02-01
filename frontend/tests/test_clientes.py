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


class ClienteUITests(TestCase):
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

        # Navegar a la página de clientes
        self.driver.get("http://127.0.0.1:8000/api/clientes/lista/")

    def test_1_crear_cliente(self):
        """
        Prueba la creación de un nuevo cliente de prueba.
        """
        self.driver.get("http://127.0.0.1:8000/api/clientes/lista/")

        # Hacer clic en "Agregar Cliente"
        add_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "add-cliente-btn"))
        )
        add_button.click()

        # Esperar a que aparezca el modal
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "showModal"))
        )

        # Llenar el formulario con datos del cliente de prueba
        self.driver.find_element(By.ID, "nombre").send_keys("Juan")
        self.driver.find_element(By.ID, "apellido").send_keys("Pérez")
        self.driver.find_element(By.ID, "documento").send_keys("12345678")
        self.driver.find_element(By.ID, "email").send_keys("juan.perez@example.com")
        self.driver.find_element(By.ID, "telefono").send_keys("987654321")
        self.driver.find_element(By.ID, "direccion").send_keys("Calle Falsa 123")

        # Guardar cliente
        guardar_button = self.driver.find_element(By.ID, "btnGuardarCliente")
        guardar_button.click()

        # Esperar mensaje de éxito
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
        )

        # Verificar que el cliente aparece en la tabla
        self.driver.refresh()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "clientes-table"))
        )
        cliente = self.driver.find_elements(By.XPATH, "//td[contains(text(), 'Juan')]")
        self.assertTrue(len(cliente) > 0, "El cliente de prueba no se agregó correctamente.")

    def test_2_editar_cliente(self):
        """
        Prueba la edición del cliente de prueba (Juan Pérez).
        """
        self.driver.get("http://127.0.0.1:8000/api/clientes/lista/")

        try:
            # Buscar la fila que contenga "Juan Pérez"
            fila_cliente = None
            rows = self.driver.find_elements(By.CSS_SELECTOR, "#clientes-table tbody tr")
            for row in rows:
                if "Juan Pérez" in row.text:
                    fila_cliente = row
                    break

            self.assertIsNotNone(fila_cliente, "No se encontró el cliente de prueba en la tabla.")

            # Hacer clic en el botón editar dentro de esa fila
            edit_button = fila_cliente.find_element(By.CLASS_NAME, "edit-btn")
            edit_button.click()

            # Esperar que aparezca el modal
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "showModal"))
            )

            # Editar el nombre
            nombre_field = self.driver.find_element(By.ID, "nombre")
            nombre_field.clear()
            nombre_field.send_keys("Juan Editado")

            # Guardar los cambios
            guardar_button = self.driver.find_element(By.ID, "btnGuardarCliente")
            guardar_button.click()

            # Esperar mensaje de éxito
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "swal2-success"))
            )

            # Verificar que el cliente se actualizó
            self.driver.refresh()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "clientes-table"))
            )
            cliente_actualizado = self.driver.find_elements(By.XPATH, "//td[contains(text(), 'Juan Editado')]")
            self.assertTrue(len(cliente_actualizado) > 0, "El cliente no se editó correctamente.")

        except TimeoutException as e:
            self.fail(f"Error al editar el cliente de prueba: {str(e)}")

    def test_3_eliminar_cliente(self):
        """
        Prueba la eliminación del cliente de prueba (Juan Editado).
        """
        self.driver.get("http://127.0.0.1:8000/api/clientes/lista/")

        try:
            # Buscar la fila que contenga "Juan Editado"
            fila_cliente = None
            rows = self.driver.find_elements(By.CSS_SELECTOR, "#clientes-table tbody tr")
            for row in rows:
                if "Juan Editado" in row.text:
                    fila_cliente = row
                    break

            self.assertIsNotNone(fila_cliente, "No se encontró el cliente de prueba en la tabla para eliminar.")

            # Hacer clic en el botón eliminar dentro de esa fila
            delete_button = fila_cliente.find_element(By.CLASS_NAME, "delete-btn")
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

            # Verificar que el cliente se eliminó
            self.driver.refresh()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "clientes-table"))
            )
            clientes_restantes = self.driver.find_elements(By.XPATH, "//td[contains(text(), 'Juan Editado')]")
            self.assertTrue(len(clientes_restantes) == 0, "El cliente no se eliminó correctamente.")

        except TimeoutException as e:
            self.fail(f"Error al eliminar el cliente de prueba: {str(e)}")

    def tearDown(self):
        """Cerrar el navegador después de cada prueba"""
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()
