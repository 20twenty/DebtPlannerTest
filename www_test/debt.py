import math
import common

class Debt:
    
    def __init__(self, debt_name, starting_balance, minimum_payment = None, apr = None, number_of_payments = None, payoff_progress = None):
        self.debt_name = debt_name
        self.starting_balance = starting_balance
        self.minimum_payment = minimum_payment
        self.number_of_payments = number_of_payments
        self.apr = apr
        self.payoff_progress = apr

        if minimum_payment == None and number_of_payments != None:
            self.minimum_payment = math.ceil(starting_balance / number_of_payments)
            if starting_balance % number_of_payments != 0:
                self.number_of_payments = number_of_payments + 1
        
        if number_of_payments == None and minimum_payment != None:
            self.number_of_payments = math.ceil(starting_balance / minimum_payment)
            if starting_balance % minimum_payment != 0:
                self.number_of_payments = int(self.number_of_payments + 1)
            
        if apr == None:
            self.apr = 0

        if payoff_progress == None:
            self.payoff_progress = 0

        date = common.get_datetime()
        self.debt_free_on = common.add_months(date, self.number_of_payments).strftime('%b %Y')
        self.debt_free_years_month = common.get_years_month_debt_free(self.number_of_payments)
        