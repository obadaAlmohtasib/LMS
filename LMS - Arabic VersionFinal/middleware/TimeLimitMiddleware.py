from datetime import date
import os
from django.conf import settings


YEAR = 2023 
MONTH = 12
DAY = 9
LAST_VALID_DATE = date(year=YEAR, month=MONTH, day=DAY)


MESSAGE = 'An error occurred. Our team will handle it soon.'

# Middleware is a framework of hooks into Django’s request/response processing.
# It’s a light, low-level “plugin” system for globally altering Django’s input or output
class Middleware():
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        
        # By commenting the following line, we stopped the functionality of disrupting the system after period of time.
        ### self.checkSystemValidity() 
        
        # Code to be executed for each request/response after
        # the view is called.

        return response # To complete chain of calls


    def checkSystemValidity(self):
        # comment the following line to activate the functionality again.
        return
    
        """Construct a date from a string in ISO 8601 format."""
        # YYYY-MM-DD
        # last_valid_date = date.fromisoformat(lines)
        # print(os.path.join(settings.BASE_DIR, 'GLOBAL_SETTINGS'))
        with open(os.path.join(settings.BASE_DIR, 'GLOBAL_SETTINGS.txt'), 'r+') as _file:
            data = _file.read()
            _file.seek(0)
            data = int(data) - 1
            _file.write(str(data))
            _file.truncate()

            if data <= 50:
                raise Exception('Something went wrong !')


        # print(LAST_VALID_DATE)

        # Read FROM File - Last Valid Date -
        today = date.today()
        # print(today)

        diff = (LAST_VALID_DATE - today).days
        if diff <= 0:
            print(MESSAGE)
            # raise Exception(MESSAGE)
            # raise ExceptionPage('errors/html')
            return 'errors/html'


# Soln:
# 1. Depends on date of system (May someone go back in days of the device/ or the date is incorrect), it won't work as expected
# 2. Depends on date of online service (Need internet connection),
# 3. Depends on how many times the user request the home page, it gonna work, subtract the number from file 
