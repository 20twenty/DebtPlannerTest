from selenium.webdriver.common.by import By

class BasePageLocators(object):
    """A class for home page locators. All main page locators should come here"""

    get_started_page = (By.CSS_SELECTOR, '#get_started_page')
    get_started_now = (By.CSS_SELECTOR, '#get_started_now')
    have_an_account = (By.CSS_SELECTOR, '#have_an_account')
    confirm_button = (By.CSS_SELECTOR, "[style*='display: block'] button.ui-button-text-only")

class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""

    main_page = (By.CSS_SELECTOR, '#main_page')
    onboarding_div = (By.CSS_SELECTOR, '#onboarding_div')
    confirm_button = (By.CSS_SELECTOR, "[style*='display: block'] button.ui-button-text-only")
    popup_text = (By.CSS_SELECTOR, "[style*='display: block'] .ui-dialog-content")
    delete_confirm = (By.CSS_SELECTOR, "[aria-describedby='remove_debt_dialog']:not([style*=none]) button:nth-child(1)")

#    Debt details
    add_button = (By.CSS_SELECTOR, '#add_button')
    debt_display = (By.CSS_SELECTOR, "#account_dialog #delete_account_button")
    debt_container = (By.CSS_SELECTOR, "#debt_container > div")
    edit_debt = (By.CSS_SELECTOR, '.debt_wrapper > div:nth-child(2)')
    debt_name = (By.CSS_SELECTOR, '.debt_name')
    current_balance = (By.CSS_SELECTOR, '.debt_balance')
    debt_apr = (By.CSS_SELECTOR, '.debt_apr')
    debt_minimum = (By.CSS_SELECTOR, '.debt_minimum')
    debt_payoff_progress_percent = (By.CSS_SELECTOR, '.debt_payoff_progress_percent')
    debt_payoff_progress_bar_paid = (By.CSS_SELECTOR, '.debt_payoff_progress_bar_paid[style]')
    debt_payoff_progress_bar_remaining = (By.CSS_SELECTOR, '.debt_payoff_progress_bar_remaining[style]')

#    Edit Debt dialog
    save_button = (By.CSS_SELECTOR, '#debt_dialog #save_button')
    debt_details = (By.CSS_SELECTOR, "#debt_dialog #debt_details")
    debt_name_edit = (By.CSS_SELECTOR, '#debt_name[placeholder]')
    debt_balance_edit = (By.CSS_SELECTOR, '#debt_balance[placeholder]')
    debt_minimum_edit = (By.CSS_SELECTOR, '#debt_minimum[placeholder]')
    debt_apr_edit = (By.CSS_SELECTOR, '#debt_apr[placeholder]')
    debt_position_select = (By.CSS_SELECTOR, '#position_div[style] > #debt_position_select > option')
    use_example = (By.CSS_SELECTOR, '#debt_dialog #use_example')
    has_promo = (By.CSS_SELECTOR, '#has_promo')
    #date
    promo_expires_date = (By.CSS_SELECTOR, '.promo_expires_date[placeholder]')
    year  = (By.CSS_SELECTOR, '.ui-datepicker-year')
    month = (By.CSS_SELECTOR, 'ui-datepicker-month')
    date = (By.CSS_SELECTOR, "[data-handler='selectDay']")
    promo_apr = (By.CSS_SELECTOR, '#promo_apr[placeholder]')
    month_prev = (By.CSS_SELECTOR, "[title='Prev']")
    month_next = (By.CSS_SELECTOR, "[title='Next']")
    remove_made_payment_button = (By.CSS_SELECTOR, "#individual_made_payment_display #remove_made_payment_button_img")
    debt_payment_amount = (By.CSS_SELECTOR, '.add_debt_payment_amount')
    made_debt_payment_amount = (By.CSS_SELECTOR, '.made_debt_payment_amount')
    principal_payment_calculator = (By.CSS_SELECTOR, "#principal_payment_calculator")
    total_paid_input = (By.CSS_SELECTOR, "#total_paid_input")
    interest_accrued_input = (By.CSS_SELECTOR, "#interest_accrued_input")
    new_expenses_input = (By.CSS_SELECTOR, "#new_expenses_input")
    calculate_principal = (By.CSS_SELECTOR, "#calculate_principal")
    use_plan_estimate = (By.CSS_SELECTOR, "#use_plan_estimate")
    delete = (By.CSS_SELECTOR, '#delete')
    other_options = (By.CSS_SELECTOR, '#other_options')

#    Payoff Plan
    debt_step = (By.CSS_SELECTOR, "#payment_plan_list div[id*='step']:not(.df_wrapper)")
    debt_free = (By.CSS_SELECTOR, "#payment_plan_list .df_wrapper")
    step_duration = (By.CSS_SELECTOR, ".step_duration")
    step_payment = (By.CSS_SELECTOR, "#step_table tbody tr td:nth-of-type(2)")

    remove_made_payment_button = (By.CSS_SELECTOR, "#individual_made_payment_display #remove_made_payment_button_img")
    debt_payment_amount = (By.CSS_SELECTOR, '.add_debt_payment_amount')
    debt_payment_date = (By.CSS_SELECTOR, '.add_debt_payment_date.hasDatepicker')
    made_debt_payment_amount = (By.CSS_SELECTOR, '.made_debt_payment_amount')
    principal_payment_calculator = (By.CSS_SELECTOR, "#principal_payment_calculator")
    total_paid_input = (By.CSS_SELECTOR, "#total_paid_input")
    interest_accrued_input = (By.CSS_SELECTOR, "#interest_accrued_input")
    new_expenses_input = (By.CSS_SELECTOR, "#new_expenses_input")
    calculate_principal = (By.CSS_SELECTOR, "#calculate_principal")
    use_plan_estimate = (By.CSS_SELECTOR, "#use_plan_estimate")
    delete = (By.CSS_SELECTOR, '#delete')
    other_options = (By.CSS_SELECTOR, '#other_options')

#    Strategy
    minimum_payment = (By.CSS_SELECTOR, '#minimum_payment')

#    Payoff Plan
    debt_step = (By.CSS_SELECTOR, "#payment_plan_list div[id*='step']:not(.df_wrapper)")
    debt_free = (By.CSS_SELECTOR, "#payment_plan_list .df_wrapper")
    step_number = (By.CSS_SELECTOR, ".step_number")
    step_duration = (By.CSS_SELECTOR, ".step_duration")
    step_debt_name = (By.CSS_SELECTOR, "#step_table tbody tr td:nth-of-type(1)")
    step_payment = (By.CSS_SELECTOR, "#step_table tbody tr td:nth-of-type(2)")

#    Account manage
    menu_active_account = (By.CSS_SELECTOR, '#menu_active_account')
    account_preferences = (By.CSS_SELECTOR, '#account_dialog #account_preferences')
    account_logout = (By.CSS_SELECTOR, '#account_dialog #account_logout')
    account_logout_button = (By.CSS_SELECTOR, '#account_dialog #account_logout_button')
    guest_logout_divider = (By.CSS_SELECTOR, '#guest_dialog #guest_logout_divider')
    guest_logout = (By.CSS_SELECTOR, '#guest_dialog #guest_logout')
    delete_account_divider = (By.CSS_SELECTOR, '#account_dialog #delete_account')
    delete_account = (By.CSS_SELECTOR, '#account_dialog #delete_account_button')
    delete_account_password = (By.CSS_SELECTOR, '#account_dialog #delete_account_password')

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
    validation_code_email = (By.CSS_SELECTOR, '#validation_code_email')
    validate_button = (By.CSS_SELECTOR, "[value='Validate']")
    change_email_button = (By.CSS_SELECTOR, "[value='Change Email']")

class ForgotPasswordPageLocators(object):
    """A class for forgot password page locators. All main page locators should come here"""

    forgot_password_page = (By.CSS_SELECTOR, '#forgot_password_page')
    forgot_password_cancel = (By.CSS_SELECTOR, '#forgot_password_cancel')
