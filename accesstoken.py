

from hashlib import new
import webbrowser
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
from pprint import pprint
import logging
import pandas as pd 
import datetime
import pdb

import requests
from bs4 import BeautifulSoup
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *


kws=""	
kite=""
api_k="5i48ezu1z2ypbuea"
api_s="vyozf69w4b6t4io7n4r58xmmo5qemxpk"	
access_token=""
def get_login(api_k,api_s):
	kite=KiteConnect(api_key=api_k)
	print("[*] Generate access Token:",kite.login_url())
	webbrowser.open(kite.login_url(), new=1)
	val=input ("[*] Enter your request token here:")
	data=kite.generate_session(val,api_secret=api_s)
	print(data["access_token"])
	access_token=data["access_token"]

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


