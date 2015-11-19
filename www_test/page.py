from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from element import BasePageElement
from locators import BasePageLocators
from locators import LoginPageLocators
from locators import MainPageLocators
from locators import CreateAccountPageLocators
import common

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
     
    def add_debt_parametrized(self, name, balance, minimum, apr):
        self.click(MainPageLocators.add_button)
        self.send_keys(MainPageLocators.debt_name_edit, name)
        self.send_keys(MainPageLocators.debt_balance_edit, balance)
        self.send_keys(MainPageLocators.debt_minimum_edit, minimum)
        self.send_keys(MainPageLocators.debt_apr_edit, apr)
        self.click(MainPageLocators.save_button)
        WebDriverWait(self.dpp, 2).until(EC.element_to_be_clickable(MainPageLocators.main_page))
        
    def get_debts(self):
        self.dpp.find_elements(*MainPageLocators.debt_display)
        
    def delete_debt(self):
        self.click(MainPageLocators.debt_name)
        self.click(MainPageLocators.other_options)
        self.click(MainPageLocators.delete)
        self.click(MainPageLocators.delete_confirm)
        
    def add_payment_ammount(self, amount):
        self.click(MainPageLocators.debt_name)
        self.send_keys(MainPageLocators.debt_payment_amount, str(amount))
        self.click(MainPageLocators.save_button)
        WebDriverWait(self.dpp, 2).until(EC.element_to_be_clickable(MainPageLocators.main_page)) 
    
    def remove_payment_ammount(self, all = False):
        self.click(MainPageLocators.debt_name)
        if all:
            while self.is_displayed(MainPageLocators.remove_made_payment_button, False):
                self.click(MainPageLocators.remove_made_payment_button)
        else:
            self.click(MainPageLocators.remove_made_payment_button)
        self.click(MainPageLocators.save_button)
        WebDriverWait(self.dpp, 2).until(EC.element_to_be_clickable(MainPageLocators.main_page))    
    
    def check_payment_ammount(self, amount):
        self.click(MainPageLocators.debt_name)
        actual = self.get_text(MainPageLocators.made_debt_payment_amount) 
        print "Compare amount expected %s and actual %s." % (amount, actual) 
        assert(float(amount) == float(actual))
        
    def check_debt_details(self, name, balance, apr, minimum, payoff_progress_percent):
        debt_name = self.get_text(MainPageLocators.debt_name)
        current_balance = self.get_text(MainPageLocators.current_balance).replace('$', '')
        debt_apr = self.get_text(MainPageLocators.debt_apr).replace('%', '')
        debt_minimum = self.get_text(MainPageLocators.debt_minimum).replace('$', '')
        debt_payoff_progress_percent = self.get_text(MainPageLocators.debt_payoff_progress_percent).replace('%', '')
        
        assert(name == debt_name)
        assert(float(balance) == float(current_balance))
        assert(float(debt_apr) == float(debt_apr))
        assert(float(debt_minimum) == float(debt_minimum))
        assert(int(payoff_progress_percent) == int(debt_payoff_progress_percent))
        
    def check_payment_progress(self, starting_balance, current_payment):
        debt_payoff_progress_bar_paid = self.get_attribute(MainPageLocators.debt_payoff_progress_bar_paid, "style")
        start = 'width: '
        end = '%'
        #Get paid amount
        start_position = debt_payoff_progress_bar_paid.index(start) + len(start)
        end_position = debt_payoff_progress_bar_paid.index(end) + len(end) - 1
        debt_payoff_progress_bar_paid = debt_payoff_progress_bar_paid[start_position: end_position]
        assert(int(current_payment) == int(debt_payoff_progress_bar_paid))

        if starting_balance != current_payment:
            debt_payoff_progress_bar_remaining = self.get_attribute(MainPageLocators.debt_payoff_progress_bar_remaining, "style")
            #Get remaining amount
            start_position = debt_payoff_progress_bar_remaining.index(start) + len(start)
            end_position = debt_payoff_progress_bar_remaining.index(end) + len(end) - 1
            debt_payoff_progress_bar_remaining = debt_payoff_progress_bar_remaining[start_position: end_position]
            assert(100 - int(current_payment) == int(debt_payoff_progress_bar_remaining))
        
    def check_step_details(self, step_number, debt_name, minimum_payment, number_of_payments):
        parent = self.get_elements(MainPageLocators.debt_step)[step_number]
        step_debt_name = self.get_child_element(parent, MainPageLocators.step_debt_name)
        step_payment = self.get_child_element(parent, MainPageLocators.step_payment)
        step_duration = self.get_child_element(parent, MainPageLocators.step_duration)
        
        name = self.get_text(step_debt_name)
        payment = self.get_text(step_payment).replace('$', '')
        duration = self.get_text(step_duration)
        
        assert(debt_name == name)
        assert(float(minimum_payment) == float(payment))
        if number_of_payments > 1:
            if number_of_payments > 2:
                month = ' months'
            if number_of_payments == 2:
                month = ' months'
            assert(str(number_of_payments - 1) + month == duration)
        
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

    def delete_account(self, password):
        self.click(MainPageLocators.menu_active_account)
        self.click(MainPageLocators.delete_account_divider)
        self.click(MainPageLocators.delete_account)
        self.send_keys(MainPageLocators.delete_account_password, password)
        self.click(MainPageLocators.delete_account)

    def validation_check(self, object_to_type, object_to_click, value, error_message = None):
        if object_to_type:
            self.send_keys(object_to_type, str(value)) 
        self.click(object_to_click)
        if error_message:
            actual = self.get_text(MainPageLocators.popup_text)
            print "Compare error text expected: '%s' and actual: '%s'." % (error_message, actual)
            assert(actual == error_message)
            self.click(MainPageLocators.confirm_button)
        
    def validate_debt_field(self, object, value):
        self.send_keys(object, str(value))
        self.click(MainPageLocators.save_button)
        self.click(MainPageLocators.debt_name)   
        self.click(MainPageLocators.debt_details)

