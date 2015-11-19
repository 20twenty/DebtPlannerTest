from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from random import randint
from locators import BasePageLocators
from locators import MainPageLocators
from locators import LoginPageLocators
from locators import CreateAccountPageLocators
from locators import ValidatePageLocators
from locators import ForgotPasswordPageLocators
import page
import mail
import math

# ---------------------------
# ---- Tests start here -----
# ---------------------------

def test_demo(dpp):
    base_page = page.BasePage(dpp)
    base_page.open_login_page()
    login_page = page.LoginPage(dpp)
    login_page.login("DeMo", "demo")
    main_page = page.MainPage(dpp)
    main_page.main_function()
    main_page.logout()

def test_create_demo_account(dpp):
    base_page = page.BasePage(dpp)
    base_page.open_create_account_page()
    base_page.send_keys(CreateAccountPageLocators.new_username, '1@.demo')
    base_page.send_keys(CreateAccountPageLocators.new_password, '!@#$%^&*()')
    base_page.send_keys(CreateAccountPageLocators.new_confirm_password, '!@#$%^&*()')
    base_page.click(CreateAccountPageLocators.create_account_button)
    WebDriverWait(dpp, 5).until(EC.element_to_be_clickable(ValidatePageLocators.validate_page))
    base_page.send_keys(ValidatePageLocators.validate_new_email, '2@.demo')
    base_page.click(ValidatePageLocators.change_email_button)
    WebDriverWait(dpp, 5).until(EC.text_to_be_present_in_element(ValidatePageLocators.validation_code_email, '2@.demo'))
    WebDriverWait(dpp, 5).until(EC.element_to_be_clickable(ValidatePageLocators.validate_page))
    base_page.send_keys(ValidatePageLocators.validation_code, 'demo')
    base_page.click(ValidatePageLocators.validate_button)
    WebDriverWait(dpp, 5).until(EC.element_to_be_clickable(MainPageLocators.main_page))
  
def test_guest(dpp):
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.main_function()
    dpp.refresh();
    assert(main_page.is_displayed(MainPageLocators.main_page))
    main_page.logout_guest()
  
def test_page_nav(dpp):
    base_page = page.BasePage(dpp)
    base_page.open_create_account_page()
    base_page.click(CreateAccountPageLocators.already_a_member)
    assert(base_page.is_displayed(LoginPageLocators.login_page))
    base_page.click(LoginPageLocators.forgot_password_link)
    assert(base_page.is_displayed(ForgotPasswordPageLocators.forgot_password_page))
    base_page.click(ForgotPasswordPageLocators.forgot_password_cancel)
    assert(base_page.is_displayed(LoginPageLocators.login_page))
    
    base_page.click(LoginPageLocators.use_as_guest)
    assert(base_page.is_displayed(MainPageLocators.main_page))
    main_page = page.MainPage(dpp)
    main_page.logout_guest()
    
    base_page.is_displayed(BasePageLocators.get_started_now)
    base_page.click(BasePageLocators.get_started_now)
    assert(main_page.is_displayed(MainPageLocators.main_page))
    main_page.logout_guest()
      
    base_page.open_create_account_page()
    
    base_page.click(CreateAccountPageLocators.use_as_guest2)
    assert(base_page.is_displayed(MainPageLocators.main_page))
    main_page.logout_guest()
  
def test_add_principal_payment(dpp):
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.add_debt()
    main_page.add_payment_ammount(20)
    main_page.check_payment_ammount(20)

def test_account_create(dpp):
    user = 'stiply.tone@gmail.com'
    password = 'debtPayoff!'
    
#    Mark all emails as sent
    mail.mark_seen()
    base_page = page.BasePage(dpp)
    base_page.open_create_account_page()
    base_page.send_keys(CreateAccountPageLocators.new_username, user)
    base_page.send_keys(CreateAccountPageLocators.new_password, password)
    base_page.send_keys(CreateAccountPageLocators.new_confirm_password, password)
    base_page.click(CreateAccountPageLocators.create_account_button)
    WebDriverWait(dpp, 5).until(EC.element_to_be_clickable(ValidatePageLocators.validate_page))
    
#    Get validation code
    mail.wait_email(60)
    code = mail.get_code()
    base_page.send_keys(ValidatePageLocators.validation_code, code)
    base_page.click(ValidatePageLocators.validate_button)
    main_page = page.MainPage(dpp)
    base_page.click(MainPageLocators.confirm_button)    
    WebDriverWait(dpp, 5).until(EC.element_to_be_clickable(MainPageLocators.main_page))
    main_page.delete_account(password)
    base_page.click(BasePageLocators.confirm_button)    
    
def test_delete_debt(dpp):
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.add_debt()
    assert(base_page.is_displayed(MainPageLocators.debt_name))
    main_page.delete_debt()
    assert(base_page.is_displayed(MainPageLocators.debt_name, False) != True)

def test_title(dpp):
    assert 'Debt Payoff Planner' == dpp.title

def test_debt_dialog_validation_debt_name(dpp):
    error_message = "\"Name\" cannot be blank. Please fill in this field before continuing"
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.click(MainPageLocators.add_button)
    main_page.validation_check(MainPageLocators.debt_name_edit, MainPageLocators.save_button, "", error_message)

def test_debt_dialog_validation_debt_balance(dpp):
    error_message = "\"Balance\" is out of range: 0<=Balance<=10000000"
    error_message_1 = "\"Minimum payment\" is not a valid number."
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.click(MainPageLocators.add_button)
    main_page.send_keys(MainPageLocators.debt_name_edit, "Name")
    main_page.validation_check(MainPageLocators.debt_balance_edit, MainPageLocators.save_button, "-1", error_message)
    main_page.validation_check(MainPageLocators.debt_balance_edit, MainPageLocators.save_button, "-0.01", error_message)
    main_page.validation_check(MainPageLocators.debt_balance_edit, MainPageLocators.save_button, "0", error_message_1)
    main_page.validation_check(MainPageLocators.debt_balance_edit, MainPageLocators.save_button, "0.01", error_message_1)
    main_page.validation_check(MainPageLocators.debt_balance_edit, MainPageLocators.save_button, "10000000", error_message_1)
    main_page.validation_check(MainPageLocators.debt_balance_edit, MainPageLocators.save_button, "10000001", error_message)
    
def test_debt_dialog_validation_minimum_payment(dpp):
    error_message = "\"Minimum payment\" is out of range: 0<=Minimum payment<=10000000"
    error_message_1 = "\"APR\" is not a valid number."
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.click(MainPageLocators.add_button)
    main_page.send_keys(MainPageLocators.debt_name_edit, "Name")
    main_page.send_keys(MainPageLocators.debt_balance_edit, randint(1, 10000000))
    main_page.validation_check(MainPageLocators.debt_minimum_edit, MainPageLocators.save_button, "-1", error_message)
    main_page.validation_check(MainPageLocators.debt_minimum_edit, MainPageLocators.save_button, "-0.01", error_message)
    main_page.validation_check(MainPageLocators.debt_minimum_edit, MainPageLocators.save_button, "0", error_message_1)
    main_page.validation_check(MainPageLocators.debt_minimum_edit, MainPageLocators.save_button, "0.01", error_message_1)
    main_page.validation_check(MainPageLocators.debt_minimum_edit, MainPageLocators.save_button, "10000000", error_message_1)
    main_page.validation_check(MainPageLocators.debt_minimum_edit, MainPageLocators.save_button, "10000001", error_message)
    
def test_debt_dialog_validation_apr(dpp):
    error_message = "\"APR\" is out of range: 0<=APR<=99"
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.click(MainPageLocators.add_button)
    main_page.send_keys(MainPageLocators.debt_name_edit, "Name")
    main_page.send_keys(MainPageLocators.debt_balance_edit, randint(1, 10000000))
    main_page.send_keys(MainPageLocators.debt_minimum_edit, randint(1, 10000000))
    main_page.validation_check(MainPageLocators.debt_apr_edit, MainPageLocators.save_button, "-1", error_message)
    main_page.validation_check(MainPageLocators.debt_apr_edit, MainPageLocators.save_button, "-0.01", error_message)
    main_page.validation_check(MainPageLocators.debt_apr_edit, MainPageLocators.save_button, "99.1", error_message)
    main_page.validation_check(MainPageLocators.debt_apr_edit, MainPageLocators.save_button, "100", error_message)
    main_page.validate_debt_field(MainPageLocators.debt_apr_edit, 0)
    main_page.validate_debt_field(MainPageLocators.debt_apr_edit, 0.01)
    main_page.validate_debt_field(MainPageLocators.debt_apr_edit, 0.99)
    main_page.validate_debt_field(MainPageLocators.debt_apr_edit, 1.01)
    main_page.validate_debt_field(MainPageLocators.debt_apr_edit, 99)
    
def test_debt_dialog_validation_promo_apr(dpp):
    error_message = "\"Promo APR\" is out of range: 0<=Promo APR<=99"
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.click(MainPageLocators.add_button)
    main_page.send_keys(MainPageLocators.debt_name_edit, "Name")
    main_page.send_keys(MainPageLocators.debt_balance_edit, randint(1, 10000000))
    main_page.send_keys(MainPageLocators.debt_minimum_edit, randint(1, 10000000))
    main_page.send_keys(MainPageLocators.debt_apr_edit, randint(0, 99))
    main_page.click(MainPageLocators.has_promo)
    main_page.click(MainPageLocators.promo_expires_date)
    main_page.click(main_page.get_elements(MainPageLocators.date)[randint(1, 28)])
    main_page.validation_check(MainPageLocators.promo_apr, MainPageLocators.save_button, "-1", error_message)
    main_page.validation_check(MainPageLocators.promo_apr, MainPageLocators.save_button, "-0.01", error_message)
    main_page.validation_check(MainPageLocators.promo_apr, MainPageLocators.save_button, "99.1", error_message)
    main_page.validation_check(MainPageLocators.promo_apr, MainPageLocators.save_button, "100", error_message)
    main_page.validate_debt_field(MainPageLocators.promo_apr, 0)
    main_page.validate_debt_field(MainPageLocators.promo_apr, 0.01)
    main_page.validate_debt_field(MainPageLocators.promo_apr, 0.99)
    main_page.validate_debt_field(MainPageLocators.promo_apr, 99)
    
def test_validation_principal_payment(dpp):
    payment = 10000000
    error_message = "\"Made Payment Amount\" is out of range: -10000000<=Made Payment Amount<=1000000000"
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.add_debt_parametrized("name", payment, randint(1, 10000000), randint(1, 99))
    main_page.add_payment_ammount(-10000000)
    main_page.remove_payment_ammount()
    main_page.add_payment_ammount(9999999.99)
    main_page.remove_payment_ammount()
    main_page.add_payment_ammount(-9999999.99)
    main_page.remove_payment_ammount()
    main_page.add_payment_ammount(10000000)
    main_page.remove_payment_ammount()
    main_page.add_payment_ammount(-0.01)
    main_page.add_payment_ammount(0)
    main_page.add_payment_ammount(0.01)
    main_page.click(MainPageLocators.debt_name)
    main_page.validation_check(MainPageLocators.debt_payment_amount, MainPageLocators.save_button, -10000001, error_message)
    main_page.validation_check(MainPageLocators.debt_payment_amount, MainPageLocators.save_button, 1000000001, error_message)
    
#    Check negative balance
    main_page.validation_check(MainPageLocators.debt_payment_amount, MainPageLocators.save_button, payment + 1, "Payment of " + str(payment + 1) + " would result in a negative balance")

#    Check empty payment amount field
    main_page.clear(MainPageLocators.made_debt_payment_amount)
    main_page.validation_check(None, MainPageLocators.save_button, None, "\"Made Payment Amount\" is not a valid number.")
    
def test_validation_principal_calculator_total_payment(dpp):
    payment = 10000000
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.add_debt_parametrized("name", randint(1, 10000000), randint(1, 10000000), randint(1, 99))    
    main_page.click(MainPageLocators.debt_name)
    main_page.click(MainPageLocators.principal_payment_calculator)
    main_page.click(MainPageLocators.use_plan_estimate)
    
    #Check total_paid_input field
    error_message = "\"Total Paid\" is out of range: 0<=Total Paid<=10000000"
    main_page.validation_check(MainPageLocators.total_paid_input, MainPageLocators.calculate_principal, -1, error_message)
    main_page.validation_check(MainPageLocators.total_paid_input, MainPageLocators.calculate_principal, -0.01, error_message)
    main_page.validation_check(MainPageLocators.total_paid_input, MainPageLocators.calculate_principal, 0)
    main_page.validation_check(MainPageLocators.total_paid_input, MainPageLocators.calculate_principal, 0.01)
    main_page.validation_check(MainPageLocators.total_paid_input, MainPageLocators.calculate_principal, payment + 1, error_message)
    main_page.validation_check(MainPageLocators.total_paid_input, MainPageLocators.calculate_principal, payment)
    
    #Check interest_accrued_input field
    error_message = "\"Interest accrued\" is out of range: 0<=Interest accrued<=10000000"
    main_page.validation_check(MainPageLocators.interest_accrued_input, MainPageLocators.calculate_principal, -1, error_message)
    main_page.validation_check(MainPageLocators.interest_accrued_input, MainPageLocators.calculate_principal, -0.01, error_message)
    main_page.validation_check(MainPageLocators.interest_accrued_input, MainPageLocators.calculate_principal, 0)
    main_page.validation_check(MainPageLocators.interest_accrued_input, MainPageLocators.calculate_principal, 0.01)
    main_page.validation_check(MainPageLocators.interest_accrued_input, MainPageLocators.calculate_principal, payment + 1, error_message)
    main_page.validation_check(MainPageLocators.interest_accrued_input, MainPageLocators.calculate_principal, payment)
    
    #Check new_expenses_input field
    error_message = "\"New expenses\" is out of range: 0<=New expenses<=10000000"
    main_page.validation_check(MainPageLocators.new_expenses_input, MainPageLocators.calculate_principal, -1, error_message)
    main_page.validation_check(MainPageLocators.new_expenses_input, MainPageLocators.calculate_principal, -0.01, error_message)
    main_page.validation_check(MainPageLocators.new_expenses_input, MainPageLocators.calculate_principal, 0)
    main_page.validation_check(MainPageLocators.new_expenses_input, MainPageLocators.calculate_principal, 0.01)
    main_page.validation_check(MainPageLocators.new_expenses_input, MainPageLocators.calculate_principal, payment + 1, error_message)
    main_page.validation_check(MainPageLocators.new_expenses_input, MainPageLocators.calculate_principal, payment)
    
def test_payoff_plan_estimate(dpp):
    debt_name = "payoff plan estimate"
    starting_balance = randint(1001, 10000000)
    number_of_payments = randint(1, 10)
    minimum_payment = math.ceil(starting_balance / number_of_payments) + 1
    
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.add_debt_parametrized(debt_name, starting_balance, minimum_payment, 0)
    
    main_page.check_step_details(0, debt_name, minimum_payment, number_of_payments)
    main_page.check_step_details(1, debt_name, starting_balance - minimum_payment * (number_of_payments - 1), 1)
    
def test_debt_details(dpp):
    debt_name = "debt details check"
    starting_balance = randint(1001, 10000000)
    minimum_payment = randint(1, 1000)
    apr = randint(1, 99)
    payoff_progress = 0
    
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.add_debt_parametrized(debt_name, starting_balance, minimum_payment, apr)
    
    current_balance = starting_balance
    main_page.check_debt_details(debt_name, current_balance, minimum_payment, apr, payoff_progress)
    
    #add a payment and check debt details again
    payment = float(starting_balance / randint(1, 10))
    main_page.add_payment_ammount(payment)
    current_balance = starting_balance - payment
    payoff_progress = round(payment/float(starting_balance)*100)
    main_page.check_debt_details(debt_name, current_balance, minimum_payment, apr, payoff_progress)
    
def test_payoff_progress_add_50_payments(dpp):
    starting_balance = 100
    minimum_payment = 2
    
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.add_debt_parametrized("progress test 50 principal payments", starting_balance, minimum_payment, 0)
    current_payment = 0
    while current_payment < starting_balance:    
        main_page.add_payment_ammount(minimum_payment)
        current_payment = current_payment + minimum_payment
        main_page.check_payment_progress(starting_balance, current_payment)
