from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By as By
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


