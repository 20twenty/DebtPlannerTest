from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By as By
from random import randint
from page import BasePage
from page import LoginPage
from page import MainPage
from locators import BasePageLocators
from locators import MainPageLocators
from locators import LoginPageLocators
from locators import CreateAccountPageLocators
from locators import ValidatePageLocators
from locators import ForgotPasswordPageLocators
import page
import mail

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
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.click(MainPageLocators.add_button)
    main_page.validation_check(MainPageLocators.debt_name_edit, "", "\"Name\" cannot be blank. Please fill in this field before continuing")

def test_debt_dialog_validation_debt_balance(dpp):
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.click(MainPageLocators.add_button)
    main_page.send_keys(MainPageLocators.debt_name_edit, "Name")
    main_page.validation_check(MainPageLocators.debt_balance, "-1", "\"Balance\" is out of range: 0<=Balance<=10000000")
    main_page.validation_check(MainPageLocators.debt_balance, "-0.01", "\"Balance\" is out of range: 0<=Balance<=10000000")
    main_page.validation_check(MainPageLocators.debt_balance, "0", "\"Minimum payment\" is not a valid number.")
    main_page.validation_check(MainPageLocators.debt_balance, "0.01", "\"Minimum payment\" is not a valid number.")
    main_page.validation_check(MainPageLocators.debt_balance, "10000000", "\"Minimum payment\" is not a valid number.")
    main_page.validation_check(MainPageLocators.debt_balance, "10000001", "\"Balance\" is out of range: 0<=Balance<=10000000")
    
def test_debt_dialog_validation_minimum_payment(dpp):
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.click(MainPageLocators.add_button)
    main_page.send_keys(MainPageLocators.debt_name_edit, "Name")
    main_page.send_keys(MainPageLocators.debt_balance, randint(1, 10000000))
    main_page.validation_check(MainPageLocators.debt_minimum, "-1", "\"Minimum payment\" is out of range: 0<=Minimum payment<=10000000")
    main_page.validation_check(MainPageLocators.debt_minimum, "-0.01", "\"Minimum payment\" is out of range: 0<=Minimum payment<=10000000")
    main_page.validation_check(MainPageLocators.debt_minimum, "0", "\"APR\" is not a valid number.")
    main_page.validation_check(MainPageLocators.debt_minimum, "0.01", "\"APR\" is not a valid number.")
    main_page.validation_check(MainPageLocators.debt_minimum, "10000000", "\"APR\" is not a valid number.")
    main_page.validation_check(MainPageLocators.debt_minimum, "10000001", "\"Minimum payment\" is out of range: 0<=Minimum payment<=10000000")
    
def test_debt_dialog_validation_apr(dpp):
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.click(MainPageLocators.add_button)
    main_page.send_keys(MainPageLocators.debt_name_edit, "Name")
    main_page.send_keys(MainPageLocators.debt_balance, randint(1, 10000000))
    main_page.send_keys(MainPageLocators.debt_minimum, randint(1, 10000000))
    main_page.click(MainPageLocators.has_promo)
    main_page.validation_check(MainPageLocators.debt_apr, "-1", "\"APR\" is out of range: 0<=APR<=99")
    main_page.validation_check(MainPageLocators.debt_apr, "-0.01", "\"APR\" is out of range: 0<=APR<=99")
    main_page.validation_check(MainPageLocators.debt_apr, "0", "Invalid Date:")
    main_page.validation_check(MainPageLocators.debt_apr, "0.01", "Invalid Date:")
    main_page.validation_check(MainPageLocators.debt_apr, "0.99", "Invalid Date:")
    main_page.validation_check(MainPageLocators.debt_apr, "1.01", "Invalid Date:")
    main_page.validation_check(MainPageLocators.debt_apr, "99", "Invalid Date:")
    main_page.validation_check(MainPageLocators.debt_apr, "99,1", "\"APR\" is out of range: 0<=APR<=99")
    main_page.validation_check(MainPageLocators.debt_apr, "100", "\"APR\" is out of range: 0<=APR<=99")
    
def test_debt_dialog_validation_apr(dpp):
    base_page = page.BasePage(dpp)
    base_page.open_main_page_as_guest()
    main_page = page.MainPage(dpp)
    main_page.click(MainPageLocators.add_button)
    main_page.send_keys(MainPageLocators.debt_name_edit, "Name")
    main_page.send_keys(MainPageLocators.debt_balance, randint(1, 10000000))
    main_page.send_keys(MainPageLocators.debt_minimum, randint(1, 10000000))
    main_page.send_keys(MainPageLocators.debt_apr, randint(0, 99))
    main_page.click(MainPageLocators.has_promo)
    main_page.click(MainPageLocators.promo_expires_date)
    main_page.click(main_page.get_elements(MainPageLocators.date)[randint(1, 28)])
    main_page.validation_check(MainPageLocators.promo_apr, "-1", "\"Promo APR\" is out of range: 0<=Promo APR<=99")
    main_page.validation_check(MainPageLocators.promo_apr, "-0.01", "\"Promo APR\" is out of range: 0<=Promo APR<=99")
    main_page.validation_check(MainPageLocators.promo_apr, "99,1", "\"Promo APR\" is out of range: 0<=Promo APR<=99")
    main_page.validation_check(MainPageLocators.promo_apr, "100", "\"Promo APR\" is out of range: 0<=Promo APR<=99")
    main_page.validate_promo_apr(0)
    main_page.validate_promo_apr(0.01)
    main_page.validate_promo_apr(0.99)
    main_page.validate_promo_apr(99)
    