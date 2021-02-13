import logging
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bot_controls import BotControls

logger = logging.getLogger(__name__)


class WalmartBot(BotControls):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.driver.get(self.product_uri)
        logger.debug("initialized")
        self.add_item_to_cart_and_checkout()
        self.fill_shipping_info()
        self.fill_out_payment_and_order()

    def add_item_to_cart_and_checkout(self):
        add_to_cart_xpath = '//*[@id="add-on-atc-container"]/div[1]/section/div[1]/div[3]/button/span/span'
        add_to_cart = {"by": By.CLASS_NAME, "value": "prod-product-cta-add-to-cart", "timeout": 5, "refresh": True}
        check_out_xpath = {
            "by": By.XPATH,
            "value": '//*[@id="cart-root-container-content-skip"]/div[1]/div/'
            "div[2]/div/div/div/div/div[3]/div/div/div[2]/div/div[2]/"
            "div/button[1]/div/div/div/div/div[3]/div/div[1]/div/"
            "section/section/div/button/span",
        }
        checkout_div = {"by": By.CLASS_NAME, "value": "cart-pos-proceed-to-checkout"}
        logger.debug("preparing to add item to cart")
        self.click_button(**add_to_cart)
        logger.debug("clicked Add to Cart")
        self.click_button(**checkout_div)
        logger.debug("clicked Checkout")
        if self.username and self.password:
            self.checkout_with_account()
        else:
            self.checkout_as_guest()

    def checkout_with_account(self):
        continue_with_account = (
            "/html/body/div[1]/div/div[1]/div/div[1]/"
            "div[3]/div/div/div/div[1]/div/div/div/div/"
            "div[3]/div/div[4]/div/section/div/section/"
            "form/div[5]/button/span"
        )
        username = '//*[@id="sign-in-email"]'
        password = (
            "/html/body/div[1]/div/div[1]/div/div[1]/div[3]/div/div/"
            "div/div[1]/div/div/div/div/div[3]/div/div[4]/div/"
            "section/div/section/form/div[2]/div/div[1]/label/"
            "div[2]/div/input"
        )
        second_continue = {"by": By.CLASS_NAME, "value": "button--primary"}
        self.enter_data(username, self.username)
        self.enter_data(password, self.password)
        self.click_button(continue_with_account)
        self.click_button(**second_continue)

    def checkout_as_guest(self):
        continue_without_account_xpath = "/html/body/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div/div[1]"
        continue_without_account = {
            "by": By.CSS_SELECTOR,
            "value": "button[data-automation-id=new-guest-continue-button]",
        }
        self.click_button(**continue_without_account)
        logger.debug("clicked Continue Without Account")

    def fill_shipping_info(self):
        if self.username and self.password:
            continue_button = "button[data-automation-id=address-book-action-buttons-on-continue]"
            self.click_button(continue_button, By.CSS_SELECTOR)
        continue_button = {"by": By.CSS_SELECTOR, "value": "button[data-automation-id=fulfillment-continue]"}
        first_name = '//*[@id="firstName"]'
        last_name = '//*[@id="lastName"]'
        email = '//*[@id="email"]'
        address = '//*[@id="addressLineOne"]'
        phone = '//*[@id="phone"]'
        confirm_info = (
            "/html/body/div[1]/div/div[1]/div/div[1]/div[3]/div/"
            "div/div/div[3]/div[1]/div[2]/div/div/div/div[3]/"
            "div/div/div/div/div/form/div[2]/div[2]/button/span"
        )
        email_opt_out = '//*[@data-automation-id="address-form-email-opt-in"]'
        logger.debug("preparing to fill shipping info")
        self.click_button(**continue_button)
        logger.debug("clicked on the first continue")
        self.enter_data(first_name, self.first_name)
        self.enter_data(last_name, self.last_name)
        self.enter_data(phone, self.phone)
        self.enter_data(email, self.email)
        self.enter_data(address, self.address)

        # Opt out of email subscriptions
        self.click_button(email_opt_out)

        logger.debug("shipping information filled")
        self.click_button(confirm_info)
        logger.debug("clicked on Confirm")

    def fill_out_payment_and_order(self):
        credit_card_num = '//*[@id="creditCard"]'
        credit_expire_month = '//*[@id="month-chooser"]'
        credit_expire_year = '//*[@id="year-chooser"]'
        credit_cvv = '//*[@id="cvv"]'
        review_order = (
            "/html/body/div[1]/div/div[1]/div/div[1]/div[3]/div/"
            "div/div/div[4]/div[1]/div[2]/div/div/div/div[3]/"
            "div[2]/div/div/div/div[2]/div/div/div/form/div[3]/"
            "div/button/span/span/span"
        )
        logger.debug("preparing to fill payment information")
        self.enter_data(credit_card_num, self.credit_number)
        self.enter_data(credit_expire_month, self.credit_month)
        self.enter_data(credit_expire_year, self.credit_year)
        self.enter_data(credit_cvv, self.credit_ccv)
        logger.debug("payment information filled")
        self.click_button(review_order)
        logger.debug("clicked Review Order")


class PS5Bot(WalmartBot):
    def __init__(self, *args, **kwargs):
        product_uri = "https://www.walmart.com/ip/PlayStation-5-Console/363472942"
        super().__init__(*args, product_uri=product_uri, **kwargs)


class PS5DigitalBot(WalmartBot):
    def __init__(self, *args, **kwargs):
        product_uri = "https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815"
        super().__init__(*args, product_uri=product_uri, **kwargs)


class MandalorianBot(WalmartBot):
    def __init__(self, *args, **kwargs):
        product_uri = "https://www.walmart.com/ip/Star-Wars-The-Vintage-Collection-The-Mandalorian/966499173"
        super().__init__(*args, product_uri=product_uri, **kwargs)
