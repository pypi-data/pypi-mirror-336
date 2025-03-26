from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class BcvFecth:
    def get(self) -> float:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # New headless mode
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
            "Safari/537.36"
        )

        driver = webdriver.Chrome(options=chrome_options)

        with driver:
            driver.get("https://www.bcv.org.ve")

            bcv_price = (
                WebDriverWait(driver, 20)
                .until(
                    ec.visibility_of_element_located(
                        (
                            By.XPATH,
                            (
                                "//div[@id='dolar']"
                                "//div[contains(@class, 'centrado')]/strong"
                            ),
                        )
                    )
                )
                .text.strip()
            )

        return round(float(bcv_price.replace(",", ".")), 2)
