from datetime import datetime,timedelta
from pprint import pprint
Weekdays = {'Monday': '3', 'Tuesday': '2',
            'Wednesday': '1', 'Thursday': '0', 'Friday': '6'}
currentDateTime = datetime.now()
Time = currentDateTime.strftime("%H:%M:%S")
Day = currentDateTime.strftime("%A")
ExpiryDate = (currentDateTime + timedelta(days=int(Weekdays[Day]))).strftime("%#m/%#d/%Y")
pprint('Expiry Date: ' + ExpiryDate + ' ' + Time + ' ' + Day)