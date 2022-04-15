

from hashlib import new
from kiteconnect import KiteConnect
from pprint import pprint
import datetime
from pushbullet import Pushbullet
import os
from datetime import datetime, timedelta
import time
import pause
# push bullet access token and variables
Pb_access_token = "o.86YtIBmZe3VMJPs94uCbC5W3DUBwEnGY"
pb = Pushbullet(Pb_access_token)
latestpush = "will get latest data in this variable"
s2 = "request_token="
flagship = 0

# kite variables
kws = ""
kite = ""
api_k = "5i48ezu1z2ypbuea"
api_s = "vyozf69w4b6t4io7n4r58xmmo5qemxpk"
access_token = ""


# code Execution will start on 9:22 morning and function CombinedDateTime is based on these value
ExecuteTime = datetime(2022, 2, 1, 9, 22, 0)
ExitTime = datetime(2022, 2, 1, 15, 29, 55)
CrendintialFlagTime = datetime(1997, 3, 1, 8, 30, 0)

# Credentials will be pushed at 8:30 morning
CrendintialFlag = -1

Weekdays_weekends = {'Monday': '1', 'Tuesday': '1',
                     'Wednesday': '1', 'Thursday': '1', 'Friday': '3', 'Saturday': '2', 'Sunday': '1'}

def CombinedDateTime(whichTime):
        Day = datetime.now().strftime("%A")
        if(whichTime == CrendintialFlagTime ):
            currdate = datetime.now().date() + \
                timedelta(days=int(Weekdays_weekends[Day]))
        else:
            currdate=datetime.now().date()
        DependentTime = whichTime.time()
        combined = datetime.combine(currdate, DependentTime)
        pb.push_note("Paused Till", combined.isoformat())
        print(combined)
        pause.until(combined)

def get_login(api_k, api_s):
    global flagship
    global data
    kite = KiteConnect(api_key=api_k)
    print("[*] Generate access Token:", kite.login_url())
    pb.push_link("Login For Access Token", kite.login_url())
    pause.minutes(45)   #Till 9:15 code will be paused and will try to read the push then
    while(flagship < 1):
        print("checking")
        latestpush = pb.get_pushes()[0]['url']
        if("request_token=" in latestpush):
            val = latestpush[latestpush.index(
                s2) + len(s2):latestpush.index(s2) + len(s2)+int(32)]
            print(val)
            flagship += 1
    data = kite.generate_session(str(val), api_secret=api_s)
    print(data["access_token"])
    access_token = data["access_token"]
    pb.delete_pushes()
    pb.push_note("Status", "logged in successfully")

    my_file = open("Credentials.py", "w")
    my_file.write("api_key=\"")
    my_file.write(str(api_k))
    my_file.write("\"")
    my_file.write("\n")
    my_file.write("api_secret=\"")
    my_file.write(api_s)
    my_file.write("\"")
    my_file.write("\n")
    my_file.write("request_token=\"")
    my_file.write(val)
    my_file.write("\"")
    my_file.write("\n")
    my_file.write("access_token=\"")
    my_file.write(access_token)
    my_file.write("\"")
    my_file.write("\n")
    my_file.close()

    CombinedDateTime(ExecuteTime)   

    if (ExecuteTime.time() < datetime.now().time() and ExitTime.time() > datetime.now().time()):
        pb.push_note("Status", "started Runnning your main Code")
        RunCmd = "python Expiry2.py"
        os.system(RunCmd)

    elif(ExitTime.time() < datetime.now().time()):
        CombinedDateTime(CrendintialFlagTime)

while(CrendintialFlag < 0):
    print(datetime.now())
    print("in while")
    if (CrendintialFlagTime.time() < datetime.now().time() and ExitTime.time() > datetime.now().time()):
        get_login(api_k, api_s)
    else:
        CombinedDateTime(CrendintialFlagTime)
