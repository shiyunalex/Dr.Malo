from datetime import datetime

def get_hour():
    return datetime.now().hour

def get_day():
    return datetime.now().weekday()

def is_weekend():
    day = get_day()
    return day == 5 or day == 6

def is_worktime():
    hour = get_hour()
    return hour >= 9 and hour <= 18



if __name__ == '__main__':
    print(is_weekend())
    print(is_worktime())