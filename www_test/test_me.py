from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By as By
from page import BasePage
from page import MainPage
from locators import BasePageLocators
from locators import MainPageLocators
from locators import LoginPageLocators
from locators import CreateAccountPageLocators
from locators import ValidatePageLocators
from locators import ForgotPasswordPageLocators

# ---------------------------
# ---- Tests start here -----
# ---------------------------

def test_demo(dpp):
    assert(dpp.find_element(*BasePageLocators.get_started_now).is_displayed()) 
    dpp.find_element(*BasePageLocators.have_an_account).click()
    assert(dpp.find_element(*LoginPageLocators.login_page).is_displayed())
    BasePage.login(dpp, "DeMo", "demo")
    MainPage.main_function(dpp)
    MainPage.logout(dpp)

def test_create_demo_account(dpp):
   BasePage.openCreateAccountPage(dpp)
   dpp.find_element(*CreateAccountPageLocators.new_username).send_keys('1@.demo')
   dpp.find_element(*CreateAccountPageLocators.new_password).send_keys('!@#$%^&*()')
   dpp.find_element(*CreateAccountPageLocators.new_confirm_password).send_keys('!@#$%^&*()')
   dpp.find_element(*CreateAccountPageLocators.new_confirm_password).submit()
   WebDriverWait(dpp, 5).until(EC.element_to_be_clickable(ValidatePageLocators.validate_page))
   dpp.find_element(*ValidatePageLocators.validate_new_email).send_keys('2@.demo')
   dpp.find_element(*ValidatePageLocators.validate_new_email).submit()
   WebDriverWait(dpp, 5).until(EC.element_to_be_clickable(ValidatePageLocators.validate_page))
   dpp.find_element(*ValidatePageLocators.validation_code).send_keys('demo')
   dpp.find_element(*ValidatePageLocators.validation_code).submit()
   WebDriverWait(dpp, 5).until(EC.element_to_be_clickable(MainPageLocators.main_page))
  
def test_guest(dpp):
   assert(dpp.find_element(*BasePageLocators.get_started_page).is_displayed())
   dpp.find_element(*BasePageLocators.get_started_now).click()
   assert(dpp.find_element(*MainPageLocators.main_page).is_displayed())
   MainPage.main_function(dpp)
   dpp.refresh();
   assert(dpp.find_element(*MainPageLocators.main_page).is_displayed())
   MainPage.logout_guest(dpp)
  
def test_page_nav(dpp):
   BasePage.openCreateAccountPage(dpp)
   dpp.find_element(*CreateAccountPageLocators.already_a_member).click()
   assert(dpp.find_element(*LoginPageLocators.login_page).is_displayed())
   dpp.find_element(*LoginPageLocators.forgot_password_link).click()
   assert(dpp.find_element(*ForgotPasswordPageLocators.forgot_password_page).is_displayed())
   dpp.find_element(*ForgotPasswordPageLocators.forgot_password_cancel).click()
   assert(dpp.find_element(*LoginPageLocators.login_page).is_displayed())
  
   dpp.find_element(*LoginPageLocators.use_as_guest).click()
   assert(dpp.find_element(*MainPageLocators.main_page).is_displayed())
   MainPage.logout_guest(dpp)
  
   dpp.find_element(*BasePageLocators.get_started_now).click()
   assert(dpp.find_element(*MainPageLocators.main_page).is_displayed())
   MainPage.logout_guest(dpp)
     
   BasePage.openCreateAccountPage(dpp)
  
   dpp.find_element(*CreateAccountPageLocators.use_as_guest2).click()
   assert(dpp.find_element(*MainPageLocators.main_page).is_displayed())
   MainPage.logout_guest(dpp)
  
def test_title(dpp):
   assert 'Debt Payoff Planner' == dpp.title


