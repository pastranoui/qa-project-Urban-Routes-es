import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import json
import time

def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""


    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    phone_field = (By.CSS_SELECTOR, '#phone')
    message_field = (By.CSS_SELECTOR, '#comment')
    button_manta_pañuelos = (By.XPATH,
    "//div[contains(text(),'Manta y pañuelos')]/../div[@class='r-sw']/div[@class='switch']/span[@class='slider round']")
    checkbox_manta_pañuelos = (By.XPATH,
    "//div[contains(text(),'Manta y pañuelos')]/../div[@class='r-sw']/div[@class='switch']/input[@class='switch-input']")
    ice_cream_plus_button = (By.XPATH,"//div[contains(@class, 'r-counter-container')][.//div[@class='r-counter-label' and text()='Helado']]//div[contains(@class, 'counter-plus')]")
    ice_cream_counter_value = (By.XPATH,"//div[contains(@class, 'r-counter-container')]//div[contains(@class, 'counter-value')]")
    modal_pedir_taxi_button = (By.XPATH, "//span[@class='smart-button-main']")
    modal_new_window_confirmation =(By.XPATH, "//div[@class = 'order-header-title']")
    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_comfort(self):
        taxi_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Pedir un taxi']")))
        taxi_button.click()
        comfort_tariff = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'tcard-title') and text()='Comfort']")))
        comfort_tariff.click()

    def set_phone_number(self, phone_number):
        button_phone_number = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".np-text")))
        button_phone_number.click()
        campo_telefono = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#phone")))
        campo_telefono.send_keys(phone_number)
        button_siguiente = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Siguiente']")))
        button_siguiente.click()
        campo_codigo = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#code")))
        codigo_phone_number = retrieve_phone_code(self.driver)
        campo_codigo.send_keys(codigo_phone_number)
        button_confirmar = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Confirmar']")))
        button_confirmar.click()
    def get_phone_number(self):
        return self.driver.find_element(*self.phone_field).get_property('value')

    def set_payment_card(self, card_number, card_code):
        button_payment_card = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.pp-value-text')))
        button_payment_card.click()
        button_agregar_tarjeta = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")))
        button_agregar_tarjeta.click()
        campo_card_number = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#number")))
        campo_card_number.send_keys(card_number)
        campo_card_number.send_keys(Keys.TAB)
        campo_card_code = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".card-code-input #code")))
        campo_card_code.send_keys(card_code)
        time.sleep(5)
        payment_modal_background = self.driver.find_element(By.TAG_NAME, "body")
        payment_modal_background.click()
        button_add_payment_card = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".pp-buttons .button.full[type='submit']")))
        button_add_payment_card.click()

        buttons_close_modal = self.driver.find_elements(By.XPATH,
       "//div[@class='section active']//button[@class='close-button section-close']")

        for button_close in buttons_close_modal:
          if button_close.is_displayed():
            button_close.click()
            break
    def set_message_for_driver(self, message_for_driver):
        button_message_driver = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#comment")))
        button_message_driver.send_keys(message_for_driver)

    def get_message_for_driver(self):
        return self.driver.find_element(*self.message_field).get_property('value')

    def set_ask_for_manta_pañuelos(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.button_manta_pañuelos)).click()

    def set_click_ice_cream_plus(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ice_cream_plus_button)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ice_cream_plus_button)).click()
    def get_ice_cream_counter_value(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ice_cream_counter_value)).text
    def set_modal_pedir_taxi(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.modal_pedir_taxi_button)).click()

    def get_order_header_title_modal(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.modal_new_window_confirmation)).text


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(5)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_set_comfort_tariff(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(5)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.set_comfort()
        active_tariff = self.driver.find_element(By.CSS_SELECTOR, '.tcard.active')
        assert 'active' in active_tariff.get_attribute('class')

    def test_set_phone_number(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(5)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.set_comfort()
        routes_page.set_phone_number(data.phone_number)
        assert routes_page.get_phone_number() == data.phone_number

    def test_set_payment_card(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(5)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.set_comfort()
        routes_page.set_payment_card(data.card_number, data.card_code)

    def test_set_message_driver(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(5)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.set_comfort()
        routes_page.set_message_for_driver(data.message_for_driver)
        assert routes_page.get_message_for_driver() == data.message_for_driver

    def test_set_ask_for_manta_pañuelos(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(5)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.set_comfort()
        routes_page.set_ask_for_manta_pañuelos()
        checkbox_manta_pañuelos = self.driver.find_element(*routes_page.checkbox_manta_pañuelos)
        assert checkbox_manta_pañuelos.is_selected()

    def test_set_click_ice_cream_plus(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(5)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.set_comfort()
        routes_page.set_click_ice_cream_plus()
        assert '2' in routes_page.get_ice_cream_counter_value()

    def test_order_taxi_scenario(self):
     self.driver.get(data.urban_routes_url)
     time.sleep(5)
     routes_page = UrbanRoutesPage(self.driver)
     address_from = data.address_from
     address_to = data.address_to
     routes_page.set_route(address_from, address_to)
     routes_page.set_comfort()
     routes_page.set_phone_number(data.phone_number)
     routes_page.set_payment_card(data.card_number, data.card_code)
     routes_page.set_message_for_driver(data.message_for_driver)
     routes_page.set_ask_for_manta_pañuelos()
     checkbox_manta_pañuelos = self.driver.find_element(*routes_page.checkbox_manta_pañuelos)
     assert checkbox_manta_pañuelos.is_selected()
     routes_page.set_click_ice_cream_plus()
     routes_page.set_modal_pedir_taxi()
     assert  'Buscar automóvil' == routes_page.get_order_header_title_modal()



    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

