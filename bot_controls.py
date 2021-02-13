import time
import os
import logging
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


class BotControls:
    def __init__(
        self,
        first_name,
        last_name,
        email,
        address,
        phone,
        credit_number,
        credit_month,
        credit_year,
        credit_ccv,
        username=None,
        password=None,
        chrome_path=None,
        chrome_path_var=None,
        product_uri=None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.phone = phone
        self.credit_number = credit_number
        self.credit_month = credit_month
        self.credit_year = credit_year
        self.credit_ccv = credit_ccv
        self.username = username
        self.password = password
        self.product_uri = product_uri

        if chrome_path:
            self.driver = webdriver.Chrome(chrome_path)
        elif chrome_path_var:
            self.driver = webdriver.Chrome(os.getenv(chrome_path_var))
        else:
            raise RuntimeError("Selenium Chrome driver path not set")

    @staticmethod
    def rand_sleep():
        """
        Randomize the sleep timer to throw off bot detection
        """
        time.sleep(random.uniform(0.75, 1.5))

    def click_button(self, value, by=By.XPATH, timeout=1, refresh=False):
        self.check_for_captcha()
        try:
            button = self.driver.find_element(by, value)
            time.sleep(1)
            button.click()
        except NoSuchElementException:
            logger.debug("Waiting for element to be available")
            self.rand_sleep()
            if refresh:
                logger.info("Refreshing page")
                self.driver.refresh()
            self.click_button(value, by, timeout, refresh)
        except Exception:
            logger.exception("Encountered an error clicking button, will retry in 1s")
            time.sleep(timeout)
            self.click_button(value, by)

    def enter_data(self, field, data):
        self.check_for_captcha()
        try:
            self.driver.find_element_by_xpath(field).send_keys(data)
            pass
        except NoSuchElementException:
            logger.debug("Waiting for element to be available")
            self.rand_sleep()
            self.enter_data(field, data)
        except Exception:
            time.sleep(1)
            self.enter_data(field, data)

    def check_for_captcha(self):
        while True:
            captcha = self.locate_captchas()
            if captcha and captcha.is_enabled() and captcha.is_displayed():
                logger.warning("Captcha triggered, please handle manually")
                time.sleep(1)
                continue
            else:
                break

    def locate_captchas(self):
        captcha = None
        captcha_ids = ["bot-handling-challenge", "re-captcha"]
        for captcha_id in captcha_ids:
            try:
                captcha = self.driver.find_element_by_class_name(captcha_id)
                return captcha
            except NoSuchElementException:
                pass
        return captcha
