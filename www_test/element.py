from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium import webdriver

class BasePageElement(object):
    """Base page class that is initialized on every page object class."""

    def __init__(self, dpp):
        self.dpp = dpp

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_name(self.locator))
        element = driver.find_element_by_name(self.locator)
        return element.get_attribute("value")

    def get_element(self, obj):
        try:
            WebDriverWait(self.dpp, 25).until(
                lambda driver: self.dpp.find_element(*obj))
        finally:
            WebDriverWait(self.dpp, 5).until(
                lambda driver: self.dpp.find_element(*obj))
        WebDriverWait(self.dpp, 5).until(EC.element_to_be_clickable(obj))
        return self.dpp.find_element(*obj)
    
    def click(self, obj):
        element = self.get_element(obj)
        webdriver.ActionChains(self.dpp).move_to_element(element).click(element).perform()
        
    def send_keys(self, obj, text):
        element = self.get_element(obj)
        webdriver.ActionChains(self.dpp).move_to_element(element).send_keys_to_element(element, text).perform()
        
    def is_displayed(self, obj):
        element = self.get_element(obj)
        return self.get_element(obj).is_displayed()
        