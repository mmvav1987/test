import allure
import pytest
import logging
from selenium import webdriver
from pages.main_page import MainPage

@pytest.fixture(scope="module")
def driver():
    """Фикстура для инициализации и завершения работы драйвера."""
    options = webdriver.FirefoxOptions()
    options.set_preference("network.proxy.type", 0)

    driver = webdriver.Firefox(options=options)
    yield driver
    driver.quit()

@allure.feature("Поиск на сайте Rossko")
@allure.story("Поиск товара по названию 'Аккумулятор'")
def test_search_product(driver):
    """Тест поиска товара по названию 'Аккумулятор'."""
    main_page = MainPage(driver)

    with allure.step("Открыть сайт Rossko"):
        main_page.open()

    with allure.step("Принять выбор города"):
        main_page.accept_city_selection()

    with allure.step("Нажать на элемент 'По товару'"):
        main_page.click_product_search_link()

    with allure.step("Ввести слово 'Аккумулятор' в поле поиска"):
        main_page.enter_search_term("Аккумулятор")

    with allure.step("Нажать на кнопку поиска"):
        main_page.click_search_button()

    with allure.step('Проверить, что все товарные группы называются "Аккумулятор"'):
        results = main_page.get_search_results()
        incorrect_values = [value for value in results if value != "Аккумулятор"]
        assert not incorrect_values, f"Найдены лишние значения: {incorrect_values}"

@allure.feature("Поиск на сайте Rossko")
@allure.story("Поиск товара по названию 'Масло синтетическое'")
def test_negative_search_product(driver):
    """Негативный тест поиска товара по названию 'Масло синтетическое'."""
    main_page = MainPage(driver)

    with allure.step("Открыть сайт Rossko"):
        main_page.open()

    with allure.step("Принять выбор города"):
        main_page.accept_city_selection()

    with allure.step("Нажать на элемент 'По товару'"):
        main_page.click_product_search_link()

    with allure.step("Ввести слово 'Масло синтетическое' в поле поиска"):
        main_page.enter_search_term("Масло синтетическое")

    with allure.step("Нажать на кнопку поиска"):
        main_page.click_search_button()

    with allure.step('Проверить, что все товарные группы называются "Масло синтетическое"'):
        results = main_page.get_search_results()
        incorrect_values = [value for value in results if value != "Масло синтетическое"]
        assert not incorrect_values, f"Найдены лишние значения: {incorrect_values}"
