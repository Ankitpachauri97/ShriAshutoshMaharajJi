

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
#push bullet access token and variables
# Pb_access_token = "o.Xql9PkQ9h5VbdmpfO9Oe3gf3iShKdhvy"
# pb = Pushbullet(Pb_access_token)
latestpush = "will get latest data in this variable"
s2 = "request_token="
flagship = 0

#kite variables
kws=""	
kite=""
api_k="5i48ezu1z2ypbuea"
api_s="vyozf69w4b6t4io7n4r58xmmo5qemxpk"	
access_token=""

def get_login(api_k,api_s):
	global flagship
	kite=KiteConnect(api_key=api_k)
	print("[*] Generate access Token:",kite.login_url())
	# device = pb.devices[0]
	# pb.push_link("Login For Access Token",kite.login_url())
	# pb.push_sms(device, "+917073610036", kite.login_url())
	# while(flagship<1):
	# 	print("checking")
	# 	latestpush = pb.get_pushes()[0]['url']
	# 	if("request_token=" in latestpush):
	# 		val = latestpush[latestpush.index(s2) + len(s2):latestpush.index(s2) + len(s2)+int(32)]
	# 		print(val)
	# 		flagship+=1
	# 		pb.delete_pushes
	val = input("Enter your value: ")
	data=kite.generate_session(str(val),api_secret=api_s)
	print(data["access_token"])
	access_token=data["access_token"]
	# pb.delete_pushes()
	# pb.push_note("Status","logged in successfully")

	my_file = open("Credentials.py", "w")
	my_file.write("api_key=\"")
	my_file.write(str(api_k))
	my_file.write("\"")
	my_file.write("\n")
	my_file.write("api_secret=\"")
	my_file.write(api_s )
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
	
get_login(api_k,api_s)


