from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from element import BasePageElement
from locators import BasePageLocators
from locators import LoginPageLocators
from locators import MainPageLocators
from locators import CreateAccountPageLocators

class BasePage(BasePageElement):
    """Base class to initialize the base page that will be called from all pages"""

    def open_login_page(self):
        assert(self.is_displayed(BasePageLocators.get_started_now)) 
        self.click(BasePageLocators.have_an_account)
        assert(self.is_displayed(LoginPageLocators.login_page))
    
    def open_main_page_as_guest(self):
        assert(self.is_displayed(BasePageLocators.get_started_page))
        self.dpp.find_element(*BasePageLocators.get_started_now).click()
        assert(self.is_displayed(MainPageLocators.main_page))    

    def open_create_account_page(self):
        assert(self.is_displayed(BasePageLocators.get_started_page))
        self.click(BasePageLocators.have_an_account)
        assert(self.is_displayed(LoginPageLocators.login_page))
        self.click(LoginPageLocators.create_new_account)
        assert(self.is_displayed(CreateAccountPageLocators.create_account_page))

class LoginPage(BasePage):
    """Login page action methods come here."""
    
    def login(self, username, password):
        self.send_keys(LoginPageLocators.username, username)
        self.send_keys(LoginPageLocators.password, password)
        self.click(LoginPageLocators.login_button)
        WebDriverWait(self.dpp, 5).until(EC.element_to_be_clickable(MainPageLocators.main_page))

class MainPage(BasePage):
    """Home page action methods come here."""
    
    def main_function(self):
        self.add_debt()
        self.add_debt()
        self.add_debt()
        
    def add_debt(self):
        self.click(MainPageLocators.add_button)
        self.click(MainPageLocators.use_example)
        self.click(MainPageLocators.save_button)
        WebDriverWait(self.dpp, 2).until(EC.element_to_be_clickable(MainPageLocators.main_page))
        
    def get_depts(self):
        debt_display = self.dpp.find_elements(*MainPageLocators.debt_display)
        
    def del_dept(self, name):
        debt_display = self.get_depts()
        for dept in debt_display:
            if dept.find_element(*MainPageLocators.debt_name).contains("name"):
                dept.find_element(*MainPageLocators.debt_name).click()
                dept.find_element(*MainPageLocators.other_options).click()
                dept.find_element(*MainPageLocators.delete).click()
        
    def add_payment_ammount(self, amount):
        self.click(MainPageLocators.debt_name)
        self.send_keys(MainPageLocators.debt_payment_amount, amount)
        self.click(MainPageLocators.save_button)
        WebDriverWait(self.dpp, 2).until(EC.element_to_be_clickable(MainPageLocators.main_page)) 
        
    def logout(self):
        self.click(MainPageLocators.menu_active_account)
        self.click(MainPageLocators.account_logout)
        self.click(MainPageLocators.account_logout_button)
        assert(self.is_displayed(LoginPageLocators.login_page))

    def logout_guest(self):
        self.click(MainPageLocators.menu_active_account)
        self.click(MainPageLocators.guest_logout_divider)
        self.click(MainPageLocators.guest_logout)
        assert(self.is_displayed(BasePageLocators.get_started_page))

