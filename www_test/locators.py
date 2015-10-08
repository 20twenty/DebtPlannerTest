from selenium.webdriver.common.by import By

class BasePageLocators(object):
    """A class for home page locators. All main page locators should come here"""
    
    get_started_page = (By.CSS_SELECTOR, '#get_started_page')
    get_started_now = (By.CSS_SELECTOR, '#get_started_now')
    have_an_account = (By.CSS_SELECTOR, '#have_an_account')

class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    
    main_page = (By.CSS_SELECTOR, '#main_page')
    onboarding_div = (By.CSS_SELECTOR, '#onboarding_div')
    menu_active_account = (By.CSS_SELECTOR, '#menu_active_account')
    account_preferences = (By.CSS_SELECTOR, '#account_dialog #account_preferences')
    account_logout = (By.CSS_SELECTOR, '#account_dialog #account_logout')
    account_logout_button = (By.CSS_SELECTOR, '#account_dialog #account_logout_button')
    add_button = (By.CSS_SELECTOR, '#add_button')
    use_example = (By.CSS_SELECTOR, '#debt_dialog #use_example')
    save_button = (By.CSS_SELECTOR, '#debt_dialog #save_button')
    guest_logout_divider = (By.CSS_SELECTOR, '#guest_dialog #guest_logout_divider')
    guest_logout = (By.CSS_SELECTOR, '#guest_dialog #guest_logout')
    debt_display = (By.CSS_SELECTOR, "[id*='debt_display']")
    debt_name = (By.CSS_SELECTOR, '.debt_name')
    debt_payment_amount = (By.CSS_SELECTOR, '.add_debt_payment_amount')
    other_options = (By.CSS_SELECTOR, '#other_options')
    delete = (By.CSS_SELECTOR, '#delete')
    
class LoginPageLocators(object):
    """A class for login page locators. All main page locators should come here"""
    
    login_page = (By.CSS_SELECTOR, '#login_page')    
    username = (By.CSS_SELECTOR, '#username')
    password = (By.CSS_SELECTOR, '#password')
    login_button = (By.CSS_SELECTOR, "[value='Login']")
    create_new_account = (By.CSS_SELECTOR, '#create_new_account')
    forgot_password_link = (By.CSS_SELECTOR, '#forgot_password_link')
    use_as_guest = (By.CSS_SELECTOR, '#use_as_guest')
    
class CreateAccountPageLocators(object):
    """A class for create account page locators. All main page locators should come here"""
    
    create_account_page = (By.CSS_SELECTOR, '#create_account_page')  
    new_username = (By.CSS_SELECTOR, '#new_username')
    new_password = (By.CSS_SELECTOR, '#new_password')
    new_confirm_password = (By.CSS_SELECTOR, '#new_confirm_password')
    create_account_button = (By.CSS_SELECTOR, "[value='Create Account']")
    use_as_guest2 = (By.CSS_SELECTOR, '#use_as_guest2')
    already_a_member = (By.CSS_SELECTOR, '#already_a_member')

class ValidatePageLocators(object):
    """A class for validate page locators. All main page locators should come here"""
    
    validate_page = (By.CSS_SELECTOR, '#validate_page')
    validate_new_email = (By.CSS_SELECTOR, '#validate_new_email')
    validation_code = (By.CSS_SELECTOR, '#validation_code')
    validate_button = (By.CSS_SELECTOR, "[value='Validate']")
    change_email_button = (By.CSS_SELECTOR, "[value='Change Email']")
    
class ForgotPasswordPageLocators(object):
    """A class for forgot password page locators. All main page locators should come here"""
    
    forgot_password_page = (By.CSS_SELECTOR, '#forgot_password_page')
    forgot_password_cancel = (By.CSS_SELECTOR, '#forgot_password_cancel')
    