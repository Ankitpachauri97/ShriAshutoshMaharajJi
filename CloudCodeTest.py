

from hashlib import new
import webbrowser
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
from pprint import pprint
import logging
import pandas as pd
import datetime
import pdb
from pushbullet import Pushbullet
import os
from datetime import datetime, timedelta
import time
import pause
import Credentials
# push bullet access token and variables
Pb_access_token = "o.86YtIBmZe3VMJPs94uCbC5W3DUBwEnGY"
pb = Pushbullet(Pb_access_token)
latestpush = "will get latest data in this variable"
s2 = "request_token="
flagship = 1

# kite variables
kws = ""
kite = ""
api_k = "5i48ezu1z2ypbuea"
api_s = "vyozf69w4b6t4io7n4r58xmmo5qemxpk"
access_token = ""


# code Execution will start on 9:22 morning
ExecuteTime = datetime(2022, 2, 1, 9, 22, 0)
ExitTime = datetime(2022, 2, 1, 15, 29, 55)
CrendintialFlagTime = datetime(1997, 3, 1, 8, 30, 0)

# Credentials will be pushed at 8:30 morning
CrendintialFlag = -1

Weekdays_weekends = {'Monday': '1', 'Tuesday': '1',
                     'Wednesday': '1', 'Thursday': '1', 'Friday': '3', 'Saturday': '2', 'Sunday': '1'}

def CombinedDateTime():
        Day = datetime.now().strftime("%A")
        currdate = datetime.now().date() + \
            timedelta(days=int(Weekdays_weekends[Day]))
        credentialTime = CrendintialFlagTime.time()
        combined = datetime.combine(currdate, credentialTime)
        pb.push_link("Paused Till", combined.isoformat())
        print(combined)
        pause.until(combined)

def get_login(api_k, api_s):
    global flagship

    currdate = datetime.now().date()
    Executetime = ExecuteTime.time()
    combined = datetime.combine(currdate, Executetime)
    print(combined)
    pause.until(combined)

    if (ExecuteTime.time() < datetime.now().time() and ExitTime.time() > datetime.now().time()):
        pb.push_note("Status", "started Runnning your main Code")
        RunCmd = "python Expiry2.py"
        os.system(RunCmd)

    elif(ExitTime.time() < datetime.now().time()):
        CombinedDateTime()



# while(CrendintialFlag < 0):
#     print(datetime.now())
#     print("in while")
#     if (CrendintialFlagTime.time() < datetime.now().time() and ExitTime.time() > datetime.now().time()):
#         get_login(api_k, api_s)
#     else:
#         Day = datetime.now().strftime("%A")
#         currdate = datetime.now().date() + \
#             timedelta(days=int(Weekdays_weekends[Day]))
#         credentialTime = CrendintialFlagTime.time()
#         combined = datetime.combine(currdate, credentialTime)
#         print(combined)
#         pause.until(combined)

get_login(api_k, api_s)