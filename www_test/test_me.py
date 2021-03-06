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
import common
import debt

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
    main_page = base_page.open_main_page_as_guest()
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
    main_page = base_page.open_main_page_as_guest()
    main_page.add_debt()
    main_page.add_payment_ammount(20, common.get_datetime())
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
    WebDriverWait(dpp, 25).until(EC.element_to_be_clickable(ValidatePageLocators.validate_page))

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
    main_page = base_page.open_main_page_as_guest()
    main_page.add_debt()
    assert(base_page.is_displayed(MainPageLocators.debt_name))
    main_page.delete_debt()
    assert(base_page.is_displayed(MainPageLocators.debt_name, False) != True)
    
    main_page.add_debt()
    main_page.click(MainPageLocators.remove_button)
    main_page.click(MainPageLocators.delete_confirm)
    assert(base_page.is_displayed(MainPageLocators.debt_name, False) != True)

def test_title(dpp):
    assert 'Debt Payoff Planner' == dpp.title

def test_debt_dialog_validation_debt_name(dpp):
    error_message = "\"Name\" cannot be blank. Please fill in this field before continuing"
    base_page = page.BasePage(dpp)
    main_page = base_page.open_main_page_as_guest()
    main_page.click(MainPageLocators.add_button)
    main_page.validation_check(MainPageLocators.debt_name_edit, MainPageLocators.save_button, "", error_message)

def test_debt_dialog_validation_debt_balance(dpp):
    error_message = "\"Balance\" is out of range: 0<=Balance<=10000000"
    error_message_1 = "\"Minimum payment\" is not a valid number."
    base_page = page.BasePage(dpp)
    main_page = base_page.open_main_page_as_guest()
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
    main_page = base_page.open_main_page_as_guest()
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
    main_page = base_page.open_main_page_as_guest()
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
    main_page = base_page.open_main_page_as_guest()
    main_page.click(MainPageLocators.add_button)
    main_page.send_keys(MainPageLocators.debt_name_edit, "Name")
    main_page.send_keys(MainPageLocators.debt_balance_edit, randint(1, 10000000))
    main_page.send_keys(MainPageLocators.debt_minimum_edit, randint(1, 10000000))
    main_page.send_keys(MainPageLocators.debt_apr_edit, randint(0, 99))
    main_page.click(MainPageLocators.has_promo)
    main_page.set_date(MainPageLocators.promo_expires_date, common.get_datetime())
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
    main_page = base_page.open_main_page_as_guest()
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
    main_page.click(MainPageLocators.edit_button)
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
    main_page = base_page.open_main_page_as_guest()
    main_page.add_debt_parametrized("name", randint(1, 10000000), randint(1, 10000000), randint(1, 99))
    main_page.click(MainPageLocators.edit_button)
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

def test_debt_details(dpp):
    debt_1 = debt.Debt("payoff details check", randint(1001, 10000000), None, randint(1, 99), randint(2, 10))

    base_page = page.BasePage(dpp)
    main_page = base_page.open_main_page_as_guest()
    main_page.add_debt_parametrized(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, debt_1.apr)
    main_page.check_debt_details(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, debt_1.apr, debt_1.payoff_progress)

    #edit a debt and check details
    debt_2 = debt.Debt("payoff details edited", randint(1001, 10000000), None, randint(1, 99), randint(2, 10))
    main_page.edit_debt(debt_1.debt_name, debt_2.debt_name, debt_2.starting_balance, debt_2.minimum_payment, debt_2.apr)
    main_page.check_debt_details(debt_2.debt_name, debt_2.starting_balance, debt_2.minimum_payment, debt_2.apr, debt_2.payoff_progress)

    #add a payment and check debt details again
    payment = float(debt_2.starting_balance / randint(1, 10))
    main_page.add_payment_ammount(payment)
    current_balance = debt_2.starting_balance - payment
    debt_2.payoff_progress = round(payment/float(debt_2.starting_balance)*100)
    main_page.check_debt_details(debt_2.debt_name, current_balance, debt_2.minimum_payment, debt_2.apr, debt_2.payoff_progress)

    #add another debt
    debt_3 = debt.Debt("payoff details - two debts", randint(1001, 10000000), None, randint(1, 99), randint(2, 10))
    main_page.add_debt_parametrized(debt_3.debt_name, debt_3.starting_balance, debt_3.minimum_payment, debt_3.apr)
    main_page.check_debt_details(debt_3.debt_name, debt_3.starting_balance, debt_3.minimum_payment, debt_3.apr, debt_3.payoff_progress)

def test_ordering_of_debts(dpp):
    debt_1 = debt.Debt("debt ordering check", randint(100001, 10000000), None, randint(51, 99), randint(2, 15))

    base_page = page.BasePage(dpp)
    main_page = base_page.open_main_page_as_guest()
    main_page.add_debt_parametrized(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, debt_1.apr)
    main_page.check_debt_details(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, debt_1.apr, debt_1.payoff_progress, 0)
    main_page.check_minimum_payment(debt_1.minimum_payment)
    
    debt_2 = debt.Debt("debt ordering check second loan", randint(10, 1000), None, randint(1, 50), randint(2, 10))
    main_page.add_debt_parametrized(debt_2.debt_name, debt_2.starting_balance, debt_2.minimum_payment, debt_2.apr)
    main_page.check_debt_details(debt_2.debt_name, debt_2.starting_balance, debt_2.minimum_payment, debt_2.apr, debt_2.payoff_progress, 1)
    main_page.check_minimum_payment(debt_1.minimum_payment + debt_2.minimum_payment)

    #edit position of a debt
    main_page.edit_debt(debt_1.debt_name, None, None, None, None, 1)
    main_page.check_debt_details(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, debt_1.apr, debt_1.payoff_progress, 1)
    main_page.check_debt_details(debt_2.debt_name, debt_2.starting_balance, debt_2.minimum_payment, debt_2.apr, debt_2.payoff_progress, 0)
    main_page.check_minimum_payment(debt_1.minimum_payment + debt_2.minimum_payment)

def test_payoff_progress_add_50_payments(dpp):
    debt_1 = debt.Debt("progress test 50 principal payments", 100, 2)

    base_page = page.BasePage(dpp)
    main_page = base_page.open_main_page_as_guest()
    main_page.add_debt_parametrized(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, 0)
    current_payment = 0
    while current_payment < debt_1.starting_balance:
        main_page.add_payment_ammount(debt_1.minimum_payment)
        current_payment = current_payment + debt_1.minimum_payment
        main_page.check_payment_progress(debt_1.starting_balance, current_payment)    
    
def test_payoff_summary(dpp):
    debt_name = "payoff summary check"
    starting_balance = randint(1001, 10000000)
    number_of_payments = randint(2, 15)
    minimum_payment = math.ceil(starting_balance / number_of_payments)
    apr = randint(3, 15)
    payoff_progress = 0

    base_page = page.BasePage(dpp)
    main_page = base_page.open_main_page_as_guest()
    
    main_page.add_debt_parametrized(debt_name, starting_balance, minimum_payment, apr)
    total_interest = common.get_total_interest(starting_balance, minimum_payment, number_of_payments, apr)
    
    current_balance = starting_balance - payoff_progress
    first_month_interest = round(current_balance * apr * 0.01 / 12, 2)
    date = common.get_datetime()
    debt_free_on = common.add_months(date, number_of_payments + 1).strftime('%b %Y')
    total_of_payments = starting_balance + total_interest
    total_interest_percent = round((total_interest / total_of_payments) * 100, 1)
    main_page.check_payoff_summary(current_balance, starting_balance, minimum_payment, first_month_interest, debt_free_on, number_of_payments + 1, total_of_payments, total_interest, total_interest_percent)

    #Add payment amount
    main_page.add_payment_ammount(minimum_payment)
    current_balance = starting_balance - minimum_payment
    first_month_interest = round(current_balance * apr * 0.01 / 12, 2)
    date = common.get_datetime()
    debt_free_on = common.add_months(date, number_of_payments).strftime('%b %Y')
    total_interest = common.get_total_interest(current_balance, minimum_payment, number_of_payments - 1, apr)
    total_of_payments = current_balance + total_interest
    total_interest_percent = round((total_interest / total_of_payments) * 100, 1)
    main_page.check_payoff_summary(current_balance, starting_balance, minimum_payment, first_month_interest, debt_free_on, number_of_payments, total_of_payments, total_interest, total_interest_percent)

def test_sorting_of_debts(dpp):
    debt_1 = debt.Debt("sorting of debts 1", 200, 20, 20)
    debt_2 = debt.Debt("sorting of debts 2", 300, 34, 30)
    debt_3 = debt.Debt("sorting of debts 3", 100, 10, 10)
 
    base_page = page.BasePage(dpp)
    main_page = base_page.open_main_page_as_guest()
    
    main_page.add_debt_parametrized(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, debt_1.apr)
    main_page.add_debt_parametrized(debt_2.debt_name, debt_2.starting_balance, debt_2.minimum_payment, debt_2.apr)
    main_page.add_debt_parametrized(debt_3.debt_name, debt_3.starting_balance, debt_3.minimum_payment, debt_3.apr)
    
    main_page.set_payoff_order('APR high to low')
    main_page.check_step_details(0, debt_1.debt_name, debt_1.minimum_payment, (debt_1.number_of_payments - 2), 1)
    main_page.check_step_details(0, debt_2.debt_name, debt_2.minimum_payment, (debt_1.number_of_payments - 2), 0)
    main_page.check_step_details(0, debt_3.debt_name, debt_3.minimum_payment, (debt_1.number_of_payments - 2), 2)
        
    main_page.check_step_details(1, debt_1.debt_name, 20.60, 1, 1)
    main_page.check_step_details(1, debt_2.debt_name, 3.19, 1, 0)
    main_page.check_step_details(1, debt_3.debt_name, 4.86, 1, 2)
    
    debt_free = common.get_month_debt_free(11)
    debt_free_years_month = common.get_years_month_debt_free(debt_1.number_of_payments - 1)
         
    main_page.check_step_debt_paid_payoff_plan(0, debt_2.debt_name, debt_free, debt_free_years_month)
    main_page.check_step_debt_paid_payoff_plan(1, debt_1.debt_name, debt_free, debt_free_years_month)
    main_page.check_step_debt_paid_payoff_plan(2, debt_3.debt_name, debt_free, debt_free_years_month)
    
    main_page.set_payoff_order('Balance low to high')
    main_page.check_step_details(0, debt_1.debt_name, debt_1.minimum_payment, (debt_1.number_of_payments - 2), 1)
    main_page.check_step_details(0, debt_2.debt_name, debt_2.minimum_payment, (debt_1.number_of_payments - 2), 2)
    main_page.check_step_details(0, debt_3.debt_name, debt_3.minimum_payment, (debt_1.number_of_payments - 2), 0)
    
    main_page.check_step_details(1, debt_1.debt_name, 20.60, 1, 1)
    main_page.check_step_details(1, debt_2.debt_name, 3.19, 1, 2)
    main_page.check_step_details(1, debt_3.debt_name, 4.86, 1, 0)    
    
    main_page.check_step_debt_paid_payoff_plan(2, debt_2.debt_name, debt_free, debt_free_years_month)
    main_page.check_step_debt_paid_payoff_plan(1, debt_1.debt_name, debt_free, debt_free_years_month)
    main_page.check_step_debt_paid_payoff_plan(0, debt_3.debt_name, debt_free, debt_free_years_month)
    
    main_page.set_payoff_order('As listed')
    main_page.check_step_details(0, debt_1.debt_name, debt_1.minimum_payment, (debt_1.number_of_payments - 2), 0)
    main_page.check_step_details(0, debt_2.debt_name, debt_2.minimum_payment, (debt_1.number_of_payments - 2), 1)
    main_page.check_step_details(0, debt_3.debt_name, debt_3.minimum_payment, (debt_1.number_of_payments - 2), 2)
    
    main_page.check_step_details(1, debt_1.debt_name, 20.60, 1, 0)
    main_page.check_step_details(1, debt_2.debt_name, 3.19, 1, 1)
    main_page.check_step_details(1, debt_3.debt_name, 4.86, 1, 2)
    
    main_page.check_step_debt_paid_payoff_plan(1, debt_2.debt_name, debt_free, debt_free_years_month)
    main_page.check_step_debt_paid_payoff_plan(0, debt_1.debt_name, debt_free, debt_free_years_month)
    main_page.check_step_debt_paid_payoff_plan(2, debt_3.debt_name, debt_free, debt_free_years_month)
    
def test_payoff_plan_one_month(dpp):
    debt_1 = debt.Debt("payoff_one_month", randint(1001, 10000000), None, 0, 1)

    base_page = page.BasePage(dpp)
    main_page = base_page.open_main_page_as_guest()
    main_page.add_debt_parametrized(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, debt_1.apr)
    main_page.check_step_details(0, debt_1.debt_name, debt_1.minimum_payment, (debt_1.number_of_payments))
    main_page.check_step_debt_paid(0, debt_1)
    
def test_payoff_plan_estimate(dpp):
    debt_1 = debt.Debt("payoff plan estimate", randint(1001, 10000000), None, 0, randint(2, 10))

    base_page = page.BasePage(dpp)
    main_page = base_page.open_main_page_as_guest()
    main_page.add_debt_parametrized(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, debt_1.apr)
    if debt_1.remainder:
        main_page.check_step_details(0, debt_1.debt_name, debt_1.minimum_payment, debt_1.number_of_payments - 1)
        main_page.check_step_details(1, debt_1.debt_name, debt_1.starting_balance - debt_1.minimum_payment * (debt_1.number_of_payments - 1), 1)
    else:
        main_page.check_step_details(0, debt_1.debt_name, debt_1.minimum_payment, debt_1.number_of_payments)
    main_page.check_step_debt_paid(0, debt_1)
    
def test_payoff_plan_two_debts(dpp):    
    debt_1 = debt.Debt("debt payoff plan check first debt", randint(10, 1000), None, None, randint(3, 6))
    debt_2 = debt.Debt("debt payoff plan check second debt", randint(100001, 10000000), None, None, randint(9, 15))
 
    base_page = page.BasePage(dpp)
    main_page = base_page.open_main_page_as_guest()
    main_page.add_debt_parametrized(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, debt_1.apr)
    main_page.add_debt_parametrized(debt_2.debt_name, debt_2.starting_balance, debt_2.minimum_payment, debt_2.apr)
    main_page.check_payoff(debt_1, debt_2)
    
def test_payoff_plan_two_debts_ending_same_month(dpp):
    number_of_payments = randint(3, 15)
    debt_1 = debt.Debt("debt payoff plan end same month check first debt", randint(10, 1000), None, None, number_of_payments)
    debt_2 = debt.Debt("debt payoff plan end same month check second debt", randint(100001, 10000000), None, None, number_of_payments)
 
    base_page = page.BasePage(dpp)
    main_page = base_page.open_main_page_as_guest()
    main_page.add_debt_parametrized(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, debt_1.apr)
    main_page.add_debt_parametrized(debt_2.debt_name, debt_2.starting_balance, debt_2.minimum_payment, debt_2.apr)
     
    #Check first step of payment
    debt_1_payment = debt_1.minimum_payment
    debt_2_payment = debt_2.minimum_payment
    if debt_1.remainder:
        main_page.check_step_details(0, debt_1.debt_name, debt_1.minimum_payment, (debt_1.number_of_payments - 1))
        main_page.check_step_details(0, debt_2.debt_name, debt_2.minimum_payment, (debt_1.number_of_payments - 1))
    
        #Check the last step of the first payment
        debt_1_payment = debt_1.starting_balance - debt_1.minimum_payment * (debt_1.number_of_payments - 1)
        debt_2_payment = debt_2.starting_balance - debt_2.minimum_payment * (debt_2.number_of_payments - 1)
            
        main_page.check_step_details(1, debt_1.debt_name, debt_1_payment, 1)
        if debt_2.remainder:
            main_page.check_step_details(1, debt_2.debt_name, debt_2_payment, 1)
    else:
        main_page.check_step_details(0, debt_1.debt_name, debt_1_payment, debt_1.number_of_payments)
        main_page.check_step_details(0, debt_2.debt_name, debt_2_payment, debt_2.number_of_payments)

    main_page.set_payoff_order('As listed')    
    main_page.check_step_debt_paid(0, debt_1)
    main_page.check_step_debt_paid(1, debt_2)

def test_image_pie_charts(dpp):
    debt_1 = debt.Debt("test canvas debt 1", 100, 10, 10, None, 'Auto Loan', '1st')
    debt_2 = debt.Debt("test canvas debt 2", 200, 20, 20, None, 'Student Loan', '28th')
    debt_3 = debt.Debt("test canvas debt 3", 300, 30, 30, None, 'Auto Loan', '3rd')

    base_page = page.BasePage(dpp)
    main_page = base_page.open_main_page_as_guest()
    
    main_page.add_debt_parametrized(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, debt_1.apr, debt_1.category, debt_1.payment_due_date)
    main_page.check_debt_details(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, debt_1.apr, debt_1.payoff_progress)
    main_page.verify_canvas(MainPageLocators.debt_category_chart, "test_canvas_chart_100.png")
    main_page.verify_canvas(MainPageLocators.debt_name_chart, "test_canvas_chart_100.png")
    main_page.verify_object_text(MainPageLocators.category_legend, [debt_1.category])
    main_page.verify_object_text(MainPageLocators.debts_legend, [debt_1.debt_name])
    
    main_page.add_debt_parametrized(debt_2.debt_name, debt_2.starting_balance, debt_2.minimum_payment, debt_2.apr, debt_2.category, debt_2.payment_due_date)
    main_page.check_debt_details(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, debt_1.apr, debt_1.payoff_progress)    
    main_page.verify_canvas(MainPageLocators.debt_category_chart, "test_canvas_chart_33_66.png")
    main_page.verify_canvas(MainPageLocators.debt_name_chart, "test_canvas_chart_33_66.png")
    main_page.verify_object_text(MainPageLocators.category_legend, [debt_2.category, debt_1.category])
    main_page.verify_object_text(MainPageLocators.debts_legend, [debt_2.debt_name, debt_1.debt_name])
    
    main_page.add_debt_parametrized(debt_3.debt_name, debt_3.starting_balance, debt_3.minimum_payment, debt_3.apr, debt_3.category, debt_3.payment_due_date)
    main_page.check_debt_details(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, debt_1.apr, debt_1.payoff_progress)
    main_page.verify_canvas(MainPageLocators.debt_category_chart, "test_canvas_chart_33_66.png")
    main_page.verify_canvas(MainPageLocators.debt_name_chart, "test_canvas_chart_17_33_50.png")
    main_page.verify_object_text(MainPageLocators.category_legend, [debt_1.category, debt_2.category])
    main_page.verify_object_text(MainPageLocators.debts_legend, [debt_3.debt_name, debt_2.debt_name, debt_1.debt_name])

def test_image_debt_chart(dpp):
    debt_1 = debt.Debt("test debt chart", 100, 10, 10)

    base_page = page.BasePage(dpp)
    main_page = base_page.open_main_page_as_guest()
    
    main_page.add_debt_parametrized(debt_1.debt_name, debt_1.starting_balance, debt_1.minimum_payment, debt_1.apr, debt_1.category, debt_1.payment_due_date)
    
    main_page.click(MainPageLocators.chart_button)
    main_page.verify_canvas(MainPageLocators.payoff_chart, "payoff_chart_100.png", True)
    chart_title = main_page.get_text(MainPageLocators.debt_name_chart_title)
    assert(chart_title == debt_1.debt_name)
    main_page.click(MainPageLocators.add_back_button)
    
    main_page.add_payment(20)
    main_page.click(MainPageLocators.chart_button)
    main_page.verify_canvas(MainPageLocators.payoff_chart, "payoff_chart_100-20.png", True)
    main_page.click(MainPageLocators.add_back_button)
    
    debt_2 = debt.Debt("test debt chart", 10000, 1)
    main_page.edit_debt(debt_1.debt_name, debt_2.debt_name, debt_2.starting_balance, debt_2.minimum_payment, debt_2.apr)
    main_page.add_payment(0)
    main_page.click(MainPageLocators.chart_button)
    chart_displayed = main_page.is_displayed(MainPageLocators.payoff_chart, False)
    assert(chart_displayed == False)
    
