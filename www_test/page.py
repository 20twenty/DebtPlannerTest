from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from element import BasePageElement
from locators import BasePageLocators
from locators import LoginPageLocators
from locators import MainPageLocators

class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def login(dpp, username, password):
        dpp.find_element(*LoginPageLocators.username).send_keys(username)
        dpp.find_element(*LoginPageLocators.password).send_keys(password)
        dpp.find_element(*LoginPageLocators.login_button).click()
        WebDriverWait(dpp, 5).until(EC.element_to_be_clickable(MainPageLocators.main_page))

class MainPage(BasePage):
    """Home page action methods come here."""
    
    def main_function(dpp):
        assert(dpp.find_element(*MainPageLocators.onboarding_div).is_displayed())
        MainPage.add_debt(dpp)
        MainPage.add_debt(dpp)
        assert(not dpp.find_element(*MainPageLocators.onboarding_div).is_displayed())
        MainPage.add_debt(dpp)
        
    def add_debt(dpp):
        dpp.find_element(*MainPageLocators.add_button).click()
        dpp.find_element(*MainPageLocators.use_example).click()
        dpp.find_element(*MainPageLocators.save_button).click()
        WebDriverWait(dpp, 2).until(EC.element_to_be_clickable(MainPageLocators.main_page))
        
    def logout(dpp):
        dpp.find_element(*MainPageLocators.menu_active_account).click()
        dpp.find_element(*MainPageLocators.account_logout).click()
        dpp.find_element(*MainPageLocators.account_logout_button).click()
        assert(dpp.find_element(*LoginPageLocators.login_page).is_displayed())

    def logout_guest(dpp):
        dpp.find_element(*MainPageLocators.menu_active_account).click()
        dpp.find_element(*MainPageLocators.guest_logout_divider).click()
        dpp.find_element(*MainPageLocators.guest_logout).click()
        assert(dpp.find_element(*BasePageLocators.get_started_page).is_displayed())

