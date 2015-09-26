from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By as By

def login(dpp, username, password):
   dpp.find_element_by_id('username').send_keys(username)
   dpp.find_element_by_id('password').send_keys(password)
   dpp.find_element_by_name('Submit').click()
   WebDriverWait(dpp, 5).until(EC.element_to_be_clickable((By.ID,'main_page')))

def logout(dpp):
   dpp.find_element_by_id('menu_active_account').click()
   dpp.find_element_by_id('account_logout').click()
   dpp.find_element_by_id('account_logout_button').click()
   assert(dpp.find_element_by_id('login_page').is_displayed())

def logout_guest(dpp):
   dpp.find_element_by_id('menu_active_account').click()
   dpp.find_element_by_id('guest_logout_divider').click()
   dpp.find_element_by_id('guest_logout').click()
   assert(dpp.find_element_by_id('get_started_page').is_displayed())

def add_debt(dpp):
   dpp.find_element_by_id('add_button').click()
   dpp.find_element_by_id('use_example').click()
   dpp.find_element_by_id('save_button').click()
   WebDriverWait(dpp, 2).until(EC.element_to_be_clickable((By.ID,'main_page')))

def main_function(dpp):
   assert(dpp.find_element_by_id('onboarding_div').is_displayed())
   add_debt(dpp)
   add_debt(dpp)
   assert(not dpp.find_element_by_id('onboarding_div').is_displayed())
   add_debt(dpp)
   

# ---------------------------
# ---- Tests start here -----
# ---------------------------

def test_demo(dpp):
   assert(dpp.find_element_by_id('get_started_page').is_displayed()) 
   dpp.find_element_by_id('have_an_account').click()
   assert(dpp.find_element_by_id('login_page').is_displayed())

   login(dpp, "DeMo", "demo")
   main_function(dpp)
   logout(dpp)

def test_guest(dpp):
   assert(dpp.find_element_by_id('get_started_page').is_displayed()) 
   dpp.find_element_by_id('get_started_now').click()
   assert(dpp.find_element_by_id('main_page').is_displayed())
   main_function(dpp)
   dpp.refresh();
   assert(dpp.find_element_by_id('main_page').is_displayed())
   logout_guest(dpp)

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
   logout_guest(dpp)

   dpp.find_element_by_id('get_started_now').click()
   assert(dpp.find_element_by_id('main_page').is_displayed())
   logout_guest(dpp)
   
   dpp.find_element_by_id('have_an_account').click()
   assert(dpp.find_element_by_id('login_page').is_displayed())
   dpp.find_element_by_id('create_new_account').click()
   assert(dpp.find_element_by_id('create_account_page').is_displayed())

   dpp.find_element_by_id('use_as_guest2').click()
   assert(dpp.find_element_by_id('main_page').is_displayed())
   logout_guest(dpp)

def test_title(dpp):
   assert 'Debt Payoff Planner' == dpp.title


