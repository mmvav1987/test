from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from selenium.webdriver.common.action_chains import ActionChains

class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://rossko.ru"
        self.logger = logging.getLogger(__name__)

    def open(self):
        """Открывает главную страницу сайта."""
        self.logger.info("Opening the main page")
        self.driver.get(self.url)

    def accept_city_selection(self):
        """Принимает выбор города, если появляется соответствующее окно."""
        try:
            self.logger.info("Accepting city selection")
            WebDriverWait(self.driver, 30).until(
                EC.invisibility_of_element_located((By.XPATH, "//span[contains(text(), 'Да')]"))
            )
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Да')]"))
            ).click()
        except Exception as e:
            self.logger.warning(f"City selection popup did not appear: {e}")

    def click_product_search_link(self):
        """Кликает на элемент 'По товару'."""
        self.logger.info("Clicking on 'По товару' link")
        try:
            # Ожидаем, пока элемент станет кликабельным
            element = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-call-block='narrowing.part' and contains(text(), 'По товару')]"))
            )

            # Прокручиваем страницу до элемента
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()

            # Используем JavaScript для клика, если стандартный клик не работает
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            self.logger.error(f"Failed to click on 'По товару' link: {e}")
            self.driver.save_screenshot("error_click_product_search_link.png")
            raise

    def enter_search_term(self, term):
        """Вводит текст в поле поиска."""
        self.logger.info(f"Entering search term: {term}")
        try:
            search_field = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input.form-field.not-filled[data-field-input='narrowing-part']"))
            )
            search_field.click()
            search_field.send_keys(term)
        except Exception as e:
            self.logger.error(f"Failed to enter search term: {e}")
            self.driver.save_screenshot("error_enter_search_term.png")
            raise

    def click_search_button(self):
        """Кликает на кнопку поиска."""
        self.logger.info("Clicking on search button")
        try:
            search_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            search_button.click()
        except Exception as e:
            self.logger.error(f"Failed to click search button: {e}")
            self.driver.save_screenshot("error_click_search_button.png")
            raise

    def get_search_results(self):
        """Возвращает список результатов поиска."""
        self.logger.info("Getting search results")
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.parts'))
            )
            result_search = self.driver.find_elements(By.CSS_SELECTOR, 'tr td:nth-child(4n)')
            return [element.text for element in result_search]
        except Exception as e:
            self.logger.error(f"Failed to get search results: {e}")
            self.driver.save_screenshot("error_get_search_results.png")
            raise
