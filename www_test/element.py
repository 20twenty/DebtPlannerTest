from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

class BasePageElement(object):
    """Base page class that is initialized on every page object class."""

    def __init__(self, dpp):
        self.dpp = dpp

    def get_text(self, obj):
        """Gets the text of the specified object"""
        element = self.get_element(obj)
        value = element.get_attribute("value")
        text = element.text
        if value:
            return value
        return text

    def get_element(self, obj):
        """Returns an element of specified object"""
        if type(obj) is WebElement:
            return obj
        try:
            WebDriverWait(self.dpp, 25).until(
                lambda driver: self.dpp.find_element(*obj))
        finally:
            WebDriverWait(self.dpp, 5).until(
                lambda driver: self.dpp.find_element(*obj))
        WebDriverWait(self.dpp, 5).until(EC.element_to_be_clickable(obj))
        return self.dpp.find_element(*obj)
    
    def get_elements(self, obj):
        """Returns an element of specified object"""
        try:
            WebDriverWait(self.dpp, 25).until(
                lambda driver: self.dpp.find_elements(*obj))
        finally:
            WebDriverWait(self.dpp, 5).until(
                lambda driver: self.dpp.find_elements(*obj))
        WebDriverWait(self.dpp, 5).until(EC.element_to_be_clickable(obj))
        return self.dpp.find_elements(*obj)
    
    def click(self, obj):
        """Clicks on the specified object"""
        element = self.get_element(obj)
        webdriver.ActionChains(self.dpp).move_to_element(element).click(element).perform()
        
    def send_keys(self, obj, text):
        """Types text to the specified object"""
        element = self.get_element(obj)
        element.clear()
        webdriver.ActionChains(self.dpp).move_to_element(element).send_keys_to_element(element, text).perform()
        
    def is_displayed(self, obj, throw_error = True):
        """Checks if the specified object is displayed"""
        if throw_error:
            self.get_element(obj)
        return self.dpp.find_element(*obj).is_displayed()
