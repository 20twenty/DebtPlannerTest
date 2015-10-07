from selenium.webdriver.common.by import By

class BasePageLocators(object):
    """A class for home page locators. All main page locators should come here"""
    
    get_started_page = (By.CSS_SELECTOR, '#get_started_page')
    get_started = (By.CSS_SELECTOR, '#get_started_now')
    login = (By.CSS_SELECTOR, '#have_an_account')

class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    
    main_page = (By.CSS_SELECTOR, '#main_page')
    onboarding_div = (By.CSS_SELECTOR, '#onboarding_div')
    menu_active_account = (By.CSS_SELECTOR, '#menu_active_account')
    account_logout = (By.CSS_SELECTOR, '#account_logout')
    account_logout_button = (By.CSS_SELECTOR, '#account_logout_button')
    add_button = (By.CSS_SELECTOR, '#add_button')
    use_example = (By.CSS_SELECTOR, '#use_example')
    save_button = (By.CSS_SELECTOR, '#save_button')
    guest_logout_divider = (By.CSS_SELECTOR, '#guest_logout_divider')
    guest_logout = (By.CSS_SELECTOR, '#guest_logout')
    
class LoginPageLocators(object):
    """A class for home page locators. All main page locators should come here"""
    
    login_page = (By.CSS_SELECTOR, '#login_page')    
    username = (By.CSS_SELECTOR, '#username')
    password = (By.CSS_SELECTOR, '#password')
    login_button = (By.CSS_SELECTOR, "[value='Login']")