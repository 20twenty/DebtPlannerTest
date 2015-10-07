from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By as By
from page import BasePage
from page import MainPage
from locators import BasePageLocators
from locators import LoginPageLocators

# ---------------------------
# ---- Tests start here -----
# ---------------------------

def test_demo(dpp):
    assert(dpp.find_element(*BasePageLocators.get_started).is_displayed()) 
    dpp.find_element(*BasePageLocators.login).click()
    assert(dpp.find_element(*LoginPageLocators.login_page).is_displayed())
    BasePage.login(dpp, "DeMo", "demo")
    MainPage.main_function(dpp)
    MainPage.logout(dpp)

def test_create_demo_account(dpp):
   assert(dpp.find_element_by_id('get_started_page').is_displayed()) 
   dpp.find_element_by_id('have_an_account').click()
   assert(dpp.find_element_by_id('login_page').is_displayed())
   dpp.find_element_by_id('create_new_account').click()
   assert(dpp.find_element_by_id('create_account_page').is_displayed())
   dpp.find_element_by_id('new_username').send_keys('1@.demo')
   dpp.find_element_by_id('new_password').send_keys('!@#$%^&*()')
   dpp.find_element_by_id('new_confirm_password').send_keys('!@#$%^&*()')
   dpp.find_element_by_id('new_confirm_password').submit()
   WebDriverWait(dpp, 5).until(EC.element_to_be_clickable((By.ID,'validate_page')))
   dpp.find_element_by_id('validate_new_email').send_keys('2@.demo')
   dpp.find_element_by_id('validate_new_email').submit()
   WebDriverWait(dpp, 5).until(EC.element_to_be_clickable((By.ID,'validate_page')))
   dpp.find_element_by_id('validation_code').send_keys('demo')
   dpp.find_element_by_id('validation_code').submit()
   WebDriverWait(dpp, 5).until(EC.element_to_be_clickable((By.ID,'main_page')))
  
def test_guest(dpp):
   assert(dpp.find_element_by_id('get_started_page').is_displayed()) 
   dpp.find_element_by_id('get_started_now').click()
   assert(dpp.find_element_by_id('main_page').is_displayed())
   MainPage.main_function(dpp)
   dpp.refresh();
   assert(dpp.find_element_by_id('main_page').is_displayed())
   MainPage.logout_guest(dpp)
  
def test_page_nav(dpp):
   assert(dpp.find_element_by_id('get_started_page').is_displayed()) 
   dpp.find_element_by_id('have_an_account').click()
   assert(dpp.find_element_by_id('login_page').is_displayed())
   dpp.find_element_by_id('create_new_account').click()
   assert(dpp.find_element_by_id('create_account_page').is_displayed())
   dpp.find_element_by_id('already_a_member').click()
   assert(dpp.find_element_by_id('login_page').is_displayed())
   dpp.find_element_by_id('forgot_password_link').click()
   assert(dpp.find_element_by_id('forgot_password_page').is_displayed())
   dpp.find_element_by_id('forgot_password_cancel').click()
   assert(dpp.find_element_by_id('login_page').is_displayed())
  
   dpp.find_element_by_id('use_as_guest').click()
   assert(dpp.find_element_by_id('main_page').is_displayed())
   MainPage.logout_guest(dpp)
  
   dpp.find_element_by_id('get_started_now').click()
   assert(dpp.find_element_by_id('main_page').is_displayed())
   MainPage.logout_guest(dpp)
     
   dpp.find_element_by_id('have_an_account').click()
   assert(dpp.find_element_by_id('login_page').is_displayed())
   dpp.find_element_by_id('create_new_account').click()
   assert(dpp.find_element_by_id('create_account_page').is_displayed())
  
   dpp.find_element_by_id('use_as_guest2').click()
   assert(dpp.find_element_by_id('main_page').is_displayed())
   MainPage.logout_guest(dpp)
  
def test_title(dpp):
   assert 'Debt Payoff Planner' == dpp.title


