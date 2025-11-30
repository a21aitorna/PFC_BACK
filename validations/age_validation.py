from datetime import date

def age_validation(birth_date):
    
    actual_day = date.today()
    age = actual_day.year - birth_date.year
    
    if actual_day.month<birth_date.month or (actual_day.month == birth_date.month and actual_day.day<birth_date.day):
        age -=1
        
    return age >=14
    