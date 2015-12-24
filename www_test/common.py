import datetime
import os
import math
import shutil
from PIL import Image

def get_number(s):
    l = []
    for t in s.split():
        try:
            l.append(float(t))
        except ValueError:
            pass
        
def get_datetime():
    return datetime.datetime.now()        

def add_months(date, months):
    month = date.month - 1 + months
    year = int(date.year + month / 12 )
    month = int(month % 12 + 1)
    #day = min(date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, date.day)

def get_years_month_debt_free(number_of_payments):
    date = get_datetime()
    year = int(date.year + number_of_payments / 12 ) - date.year
    month = int(number_of_payments % 12)
    debt_free_on = ''
    if year > 0 and year <= 1:
        debt_free_on = str(year) + ' year'
    if year > 1:
        month = month - 1
        debt_free_on = str(year) + ' years'
    if year > 0:
        debt_free_on = debt_free_on + ' '    
    if month == 1:
        debt_free_on = debt_free_on + str(month) +  ' month'
    if month > 1:
        debt_free_on = debt_free_on + str(month) + ' months'
    return debt_free_on    

def get_month_debt_free(number_of_payments):
    if number_of_payments == 1:
        debt_free_on = str(int(number_of_payments)) +  ' month'
    if number_of_payments > 1:
        debt_free_on = str(int(number_of_payments)) + ' months'
    return debt_free_on  

def get_total_interest(starting_balance, minimum_payment, number_of_payments, apr):
    count = 0
    total_interest = 0
    while (count <= number_of_payments):
        total_interest = total_interest + (starting_balance - minimum_payment * count + total_interest) * apr * 0.01 / 12
        count = count + 1
    return round(total_interest, 2)
    
def make_temp(folder):
   shutil.rmtree(folder, ignore_errors=True)
   os.makedirs(folder)

def remove_files_from_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception, e:
            print e    
    
def compare_images(img1, img2):
    h1 = Image.open(img1).histogram()
    h2 = Image.open(img2).histogram()
    print ("Comparing images, expected: " + img1 + " and actual: " + img2 + ".")
    rms = math.sqrt(sum((a-b)**2 for a,b in zip(h1, h2))/len(h1))
    print ("rms=" + str(rms));
    assert(rms < 50)
    
