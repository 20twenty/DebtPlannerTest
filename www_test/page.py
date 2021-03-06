from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from element import BasePageElement
from locators import BasePageLocators
from locators import LoginPageLocators
from locators import MainPageLocators
from locators import CreateAccountPageLocators
import time
import os
import common
from PIL import Image

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
        return MainPage(self.dpp)

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

#     def get_canvas_context(self):
#         $("#debt_category_chart")[0].getContext('2d');

    def main_function(self):
        self.add_debt()
        self.add_debt()
        self.add_debt()

    def add_debt(self):
        self.click(MainPageLocators.add_button)
        self.click(MainPageLocators.use_example)
        self.click(MainPageLocators.save_button)
        WebDriverWait(self.dpp, 2).until(EC.element_to_be_clickable(MainPageLocators.main_page))

    def set_date(self, field, date):
        if date == None:
            date = common.get_datetime()()
        self.click(field)

        #set year
        while int(self.get_text(MainPageLocators.year)) < date.year:
            self.click(MainPageLocators.month_prev)

        #set day
        self.click(self.get_element_contains_text(MainPageLocators.date, date.day))

    def add_debt_parametrized(self, name, balance, minimum, apr, category = None, payment_due_date = None):
        self.click(MainPageLocators.add_button)
        self.send_keys(MainPageLocators.debt_name_edit, name)
        self.send_keys(MainPageLocators.debt_balance_edit, str(balance))
        self.send_keys(MainPageLocators.debt_minimum_edit, str(minimum))
        self.send_keys(MainPageLocators.debt_apr_edit, str(apr))
        if category != None:
            self.select_option(MainPageLocators.debt_category, category)
        if payment_due_date != None:
            self.select_option(MainPageLocators.debt_payment_due_date, payment_due_date)
        self.click(MainPageLocators.save_button)
        WebDriverWait(self.dpp, 2).until(EC.element_to_be_clickable(MainPageLocators.main_page))

    def edit_debt(self, old_name, new_name, balance, minimum, apr, position = None):
        self.click(self.get_edit_debt_by_name(old_name))
        self.click(MainPageLocators.debt_details)
        if new_name != None:
            self.send_keys(MainPageLocators.debt_name_edit, new_name)
        if balance != None:
            self.send_keys(MainPageLocators.debt_balance_edit, str(balance))
        if minimum != None:
            self.send_keys(MainPageLocators.debt_minimum_edit, str(minimum))
        if apr != None:
            self.send_keys(MainPageLocators.debt_apr_edit, str(apr))
        if position != None:
            self.click(self.get_elements(MainPageLocators.debt_position_select)[position])
        self.click(MainPageLocators.save_button)
        WebDriverWait(self.dpp, 2).until(EC.element_to_be_clickable(MainPageLocators.main_page))

    def get_debts(self):
        self.dpp.find_elements(*MainPageLocators.debt_display)

    def delete_debt(self):
        self.click(MainPageLocators.edit_debt)
        self.click(MainPageLocators.other_options)
        self.click(MainPageLocators.delete)
        self.click(MainPageLocators.delete_confirm)

    def add_payment_ammount(self, amount, date = None):
        self.click(MainPageLocators.edit_debt)
        self.send_keys(MainPageLocators.debt_payment_amount, str(amount))
        if date != None:
            #set day
            self.set_date(MainPageLocators.debt_payment_date, date)
        self.click(MainPageLocators.save_button)
        WebDriverWait(self.dpp, 2).until(EC.element_to_be_clickable(MainPageLocators.main_page))

    def remove_payment_ammount(self, all = False):
        self.click(MainPageLocators.edit_debt)
        if all:
            while self.is_displayed(MainPageLocators.remove_made_payment_button, False):
                self.click(MainPageLocators.remove_made_payment_button)
        else:
            self.click(MainPageLocators.remove_made_payment_button)
        self.click(MainPageLocators.save_button)
        WebDriverWait(self.dpp, 2).until(EC.element_to_be_clickable(MainPageLocators.main_page))

    def check_payment_ammount(self, amount):
        self.click(MainPageLocators.edit_debt)
        actual = self.get_text(MainPageLocators.made_debt_payment_amount)
        print "Compare amount expected %s and actual %s." % (amount, actual)
        assert(float(amount) == float(actual))

    def check_minimum_payment(self, minimum_payment):
        assert(float(self.get_text(MainPageLocators.minimum_payment).replace('$','').replace(' +','')) == minimum_payment)

    def check_debt_details(self, name, balance, minimum, apr, payoff_progress_percent, position = None):
        debt_container = self.get_debt_by_name(name)
        if position != None:
            debt_container = self.get_elements(MainPageLocators.debt_container)[position]
        debt_name = self.get_text(self.get_child_element(debt_container, MainPageLocators.debt_name))
        current_balance = self.get_text(self.get_child_element(debt_container, MainPageLocators.current_balance)).replace('$', '')
        debt_apr = self.get_text(self.get_child_element(debt_container, MainPageLocators.debt_apr)).replace('%', '')
        debt_minimum = self.get_text(self.get_child_element(debt_container, MainPageLocators.debt_minimum)).replace('$', '')
        debt_payoff_progress_percent = self.get_text(self.get_child_element(debt_container, MainPageLocators.debt_payoff_progress_percent)).replace('%', '')

        assert(name == debt_name)
        assert(float(balance) == float(current_balance))
        assert(float(apr) == float(debt_apr))
        assert(float(minimum) == float(debt_minimum))
        assert(int(payoff_progress_percent) == int(debt_payoff_progress_percent))

    def get_debt_by_name(self, debt_name):
        debt_containers = self.get_elements(MainPageLocators.debt_container)
        for debt_container in debt_containers:
            if self.get_text(self.get_child_element(debt_container, MainPageLocators.debt_name)) == debt_name:
                return debt_container

    def get_edit_debt_by_name(self, debt_name):
        debt_containers = self.get_elements(MainPageLocators.debt_container)
        for debt_container in debt_containers:
            if self.get_text(self.get_child_element(debt_container, MainPageLocators.debt_name)) == debt_name:
                return self.get_child_element(debt_container, MainPageLocators.edit_debt)


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

    def add_payment(self, amount):
        self.click(MainPageLocators.planned_payment_button)
        self.send_keys(MainPageLocators.popup_input, amount)
        self.click(MainPageLocators.confirm_button)
        
    def set_payoff_order(self, order):
#         self.click(MainPageLocators.payoff_order)
        position = 0
        order = order.lower()
        if order == 'APR high to low'.lower():
            position = 0
        if order == 'Balance low to high'.lower():
            position = 1
        if order == 'As listed'.lower():
            position = 2
        element = self.get_elements(MainPageLocators.payoff_order)[position]
        self.click(element)

    def check_step_details(self, step_number, debt_name, minimum_payment, number_of_payments, index = None):
        payoff_plan_step = self.get_elements(MainPageLocators.payoff_plan_step)[step_number]
        step_duration = self.get_child_element(payoff_plan_step, MainPageLocators.payoff_plan_step_duration)
        payoff_plan_debts = self.get_child_elements(payoff_plan_step, MainPageLocators.payoff_plan_debt)
        if index == None:
            payoff_plan_debt = self.get_element_contains_text(payoff_plan_debts, debt_name)
        else:
            payoff_plan_debt = payoff_plan_debts[index]
        step_debt_name = self.get_child_element(payoff_plan_debt, MainPageLocators.payoff_plan_debt_name)
        step_payment = self.get_child_element(payoff_plan_debt, MainPageLocators.payoff_plan_payment)

        name = self.get_text(step_debt_name)
        payment = self.get_text(step_payment).replace('$', '')
        duration = self.get_text(step_duration)
        duration_expected = common.get_month_debt_free(number_of_payments)

        assert(debt_name == name)
        assert(float(minimum_payment) == float(payment))
        assert(duration_expected == duration)
    
    def check_step_debt_paid(self, step_number, debt):
        self.check_step_debt_paid_payoff_plan(step_number, debt.debt_name, debt.debt_free_on, debt.debt_free_years_month) 
        
    def check_step_debt_paid_payoff_plan(self, step_number, debt_name, debt_free_on, debt_free_years_month):
        parent = self.get_elements(MainPageLocators.debt_free)[step_number]
        debt_free_name = self.get_child_element(parent, MainPageLocators.debt_free_name)
        debt_free_duration = self.get_child_element(parent, MainPageLocators.debt_free_duration)

        name = self.get_text(debt_free_name)
        duration = self.get_text(debt_free_duration)

        assert(debt_name == name)
        assert(debt_free_on in duration)        
        assert(debt_free_years_month in duration)
        
    def check_payoff_summary(self, current_balance, starting_balance, monthly_payment, first_month_interest, debt_free_on, number_of_payments, total_of_payments, total_interest, total_interest_percent):
        current_balance_actual = self.get_text(self.get_element(MainPageLocators.payoff_current_balance)).replace('$', '')
        starting_balance_actual = self.get_text(self.get_element(MainPageLocators.starting_balance)).replace('$', '')
        monthly_payment_actual = self.get_text(self.get_element(MainPageLocators.monthly_payment)).replace('$', '')
        first_month_interest_actual = self.get_text(self.get_element(MainPageLocators.first_month_interest)).replace('$', '')
        debt_free_on_actual = self.get_text(self.get_element(MainPageLocators.debt_free_on))
        total_of_payments_actual = self.get_text(self.get_element(MainPageLocators.total_of_payments)).replace('$', '')
        total_interest_actual = self.get_text(self.get_element(MainPageLocators.total_interest)).replace('$', '')
        total_interest_percent_actual = self.get_text(self.get_element(MainPageLocators.total_interest_percent)).replace('%', '').replace('(', '').replace(')', '')
        
        assert(float(current_balance) == float(current_balance_actual))
        assert(float(starting_balance) == float(starting_balance_actual))
        assert(float(monthly_payment) == float(monthly_payment_actual))
        assert(float(first_month_interest) == float(first_month_interest_actual))
        assert(debt_free_on in debt_free_on_actual)
        debt_free_on = common.get_years_month_debt_free(number_of_payments)
        assert(debt_free_on in debt_free_on_actual)
        assert(float(total_of_payments) == float(total_of_payments_actual))
        assert(float(total_interest) == float(total_interest_actual))
        assert(float(total_interest_percent) == float(total_interest_percent_actual))   
        
    def check_payoff(self, debt_1, debt_2):
        #Check first step of payment
        debt_1_payment = debt_1.minimum_payment
        debt_2_payment = debt_2.minimum_payment
        
        step_number = 0
        if debt_1.remainder:
            step_number = 1
            self.check_step_details(0, debt_1.debt_name, debt_1.minimum_payment, (debt_1.number_of_payments - 1))
            self.check_step_details(0, debt_2.debt_name, debt_2.minimum_payment, (debt_1.number_of_payments - 1))
        
            #Check the last step of the first payment
            debt_1_payment = debt_1.starting_balance - debt_1.minimum_payment * (debt_1.number_of_payments - 1)
            debt_2_payment = debt_2.minimum_payment + debt_1.minimum_payment - debt_1_payment
                
            self.check_step_details(1, debt_1.debt_name, debt_1_payment, 1)
            if debt_2.remainder:
                self.check_step_details(1, debt_2.debt_name, debt_2_payment, 1)
        else:
            self.check_step_details(0, debt_1.debt_name, debt_1_payment, debt_1.number_of_payments)
            self.check_step_details(0, debt_2.debt_name, debt_2_payment, debt_1.number_of_payments)
        
        self.check_step_debt_paid(0, debt_1)
        
        if debt_1.number_of_payments != debt_2.number_of_payments:
            #Check first step of the second debt after payoff of the first debt
            minimum_payment = debt_2.minimum_payment + debt_1.minimum_payment
            left_to_pay = debt_2.starting_balance - (debt_2.minimum_payment * debt_1.number_of_payments + debt_1.minimum_payment - debt_1_payment)
            left_duration = int(left_to_pay / minimum_payment)
            
            if left_to_pay <= minimum_payment:
                self.check_step_details(step_number + 1, debt_2.debt_name, left_to_pay, 1)
            if left_duration > 1:
                self.check_step_details(step_number + 1, debt_2.debt_name, minimum_payment, left_duration)
                last_payment = left_to_pay - minimum_payment * left_duration
                self.check_step_details(step_number + 2, debt_2.debt_name, last_payment, 1)
                    
            debt_2.debt_free_on = common.add_months(common.get_datetime(), debt_1.number_of_payments + left_duration + 1).strftime('%b %Y')
            debt_2.debt_free_years_month = common.get_years_month_debt_free(debt_1.number_of_payments + left_duration + 1)
        self.check_step_debt_paid(1, debt_2)    
        
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

    def validate_debt_field(self, obj, value):
        self.send_keys(obj, str(value))
        self.click(MainPageLocators.save_button)
        self.click(MainPageLocators.edit_debt)
        self.click(MainPageLocators.debt_details)

    def verify_canvas(self, obj, file_expected, reverse = None):
        file_expected_path = os.path.dirname(os.path.realpath(__file__)) + os.sep + "files" + os.sep + file_expected
        file_path_folder = os.path.dirname(os.path.realpath(__file__)) + os.sep + "temp" + os.sep
        file_path = file_path_folder + str(int(time.time()*100.00)) + ".png"
        self.dpp.save_screenshot(file_path)
        canvas = self.get_element(obj)
        height = canvas.rect['height']
        width = canvas.rect['width']
        if reverse != None:
            height = canvas.rect['width']
            width = canvas.rect['height']
        x = canvas.rect['x']
        y = canvas.rect['y']
        
        image = Image.open(file_path)
        image = image.crop((x, y, x + height, y + width))
        #cropped_screenshot = file_path_folder + str(int(time.time()*100.00)) + ".png"
        cropped_screenshot = file_path_folder + file_expected 
        image.save(cropped_screenshot)

        common.compare_images(file_expected_path, cropped_screenshot)
        
