import pytest
import allure
import logging

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания отчетов и скриншотов при падении тестов."""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs["driver"]
            allure.attach(driver.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logging.getLogger(__name__).error(f"Не удалось сделать скриншот: {e}")

@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """Конфигурация логгирования для всех тестов."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("test.log"),
            logging.StreamHandler()
        ]
    )
