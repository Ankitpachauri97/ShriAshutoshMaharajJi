from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
from pprint import pprint
import logging
import pandas as pd 
import datetime
import pdb
import	json
import csv
import Credentials

#*******************************************************SETTING UP THE CONNECTION*******************************************DO NOT TOUCH*********************
#initialisation
logging.basicConfig(level=logging.DEBUG)
kite = KiteConnect(api_key=Credentials.api_key)
kws = KiteTicker(Credentials.api_key,Credentials.access_token)
kite.set_access_token(Credentials.access_token)

#*******************************************************SETTING UP THE CONNECTION*******************************************DO NOT TOUCH*********************


		#1)Get position for orders and position to develop instrument tocken and ticker dict-----------------------------------------------------------------

# hard coded the number of positions
position=kite.positions()
all_positions=position["net"]

		#*****************DEFINING variables****************************************************************************************************************
Position_tokens=[]
Positions_symbol=[]
Positions_instruementtockens=[]
Quantity=[]
Date="6/10/2021"

for n in all_positions:
	if n["product"]== "MIS" and n["sell_price"]>0 and n["quantity"]<0:
		# position_tokens[n["instrument_token"]]={"SELL":n["average_price"],"CURRENT":0,"Quantity":abs(n["quantity"]),"TRADINGSYMBOL":n["tradingsymbol"]}
		token={n["instrument_token"]:{"SELL":round(n["average_price"],1),"CURRENT":round(0,1),"QUANTITY":abs(n["quantity"]),"TRADINGSYMBOL":n["tradingsymbol"]}}
		Position_tokens.append(token)
		Positions_symbol.append(n["tradingsymbol"])
		Positions_instruementtockens.append(n["instrument_token"])
		Quantity.append(n["quantity"])
		PRODUCT_MIS_NRML=n["product"]
pprint(Position_tokens)
pprint(Positions_symbol)

position_token_LTP_FIRST=Position_tokens[0]
position_token_LTP_LAST=Position_tokens[1]
START=Positions_symbol[0]
END=Positions_symbol[1]

		#POSITIONAL TOKEN of the first and last value orders------------------------------------------------------------------------------------------------ 

instrument_first_position=Positions_instruementtockens[0]
instrument_second_position=Positions_instruementtockens[1]

		#Splitting the Position Dict for SELL and CURRENT price for fisrt instrument position and second instrument position---------------------------------

Start_value=int(START[-7:-2]) - int(450)
End_value=int(END[-7:-2])+ int(450)

		#All Strike price values in a list to develop TICKER LIST---------------------------------------------------------------------------------------------

Strike_price_list=[]
Strike_price_list.append(int(Start_value))
Factor=(int(End_value)-int(Start_value))/35
n=1
while n<Factor:
	Strike_price_list.append(int(Start_value)+50*n)
	n+=1
# print(Strike_price_list)

		#All TickerNames for all the  strike Prices-----------------------------------------------------------------------------------------------------------

Ticker=[]
for n in Strike_price_list:
	CE_Values=END[0:10]+str(n)+ END[-2:]
	PE_Values=START[0:10]+str(n)+START[-2:]
	Ticker.append(CE_Values)
	Ticker.append(PE_Values)
# print(Ticker)

		#Have developed the INSTRUMENT TOKEN LIST for the ON_CONNECT FUNCTION---------------------------------------------------------------------------------------

instrument_token_list=[]
instrument_token_list1=[]
instrument_token=[]
instrument_token1=[]


with open('bm_instruments1.txt','r') as csv_file:
	csv_reader = csv.reader(csv_file)
	next(csv_reader)
	for n in csv_reader:
		instrument_token_list.append(n[0])


for n in instrument_token_list:
	list=n.split("	")
	instrument_token_list1.append(list)

for n in Ticker:
	for k in instrument_token_list1:
		if n==k[2] and Date==str(k[5]):
			instrument_token1.append(k[0])

for n in instrument_token1:
	instrument_token.append(int(n))

# print(instrument_token)
		
		#Have developed the INSTRUMENT TOKEN DICTIONARY WITH TICKER AND TOKEN NAMES for the  ORDER PUTTING FUNCTION----------------------------------------

Ticker_Instrument_token=zip(Ticker,instrument_token)
Ticker_Instrument_token_dict=dict(Ticker_Instrument_token)

		#This is being used in if conditions for the difference between the values while executing for our strategy---------------------------------------------------------
		
Ticker_instruement_dict=dict(zip(instrument_token,Ticker))

		#Creating BUYING and SELLING functions to Place orders-----------------------------------------------------------------------------------------------

Quantity=abs(Quantity[0])
Product="kite.PRODUCT_"+PRODUCT_MIS_NRML

def ApplyOrders(buying_back,selling_lot,Quantity):
		kite.place_order(tradingsymbol=buying_back,
                                exchange=kite.EXCHANGE_NFO,
                                variety=kite.VARIETY_REGULAR,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=Quantity,
                                order_type=kite.ORDER_TYPE_MARKET,
                                product=kite.PRODUCT_MIS)

		kite.place_order(tradingsymbol=selling_lot,
                                exchange=kite.EXCHANGE_NFO,
                                variety=kite.VARIETY_REGULAR,
                                transaction_type=kite.TRANSACTION_TYPE_SELL,
                                quantity=Quantity,
                                order_type=kite.ORDER_TYPE_MARKET,
                                product=kite.PRODUCT_MIS)

def get_key(val):
    for key, value in Ticker_Instrument_token_dict.items():
        if val == value:
        	return key

# 2) ######################################################  Now setting up the live values matching algorithm  #########################################################

instrument_token_LTP=dict.fromkeys(instrument_token,"-1")

def on_ticks(ws, ticks):
	global instrument_first_position
	global instrument_second_position

	for token in ticks:
		token_value=token["instrument_token"]
		ltp=token['last_price']
		instrument_token_LTP.update({token_value:ltp})
	# print(instrument_token_LTP)

			#updating the current value of instrument which we have selled to ease down the computations-------------------------------------------------


	position_token_LTP_FIRST[instrument_first_position]["CURRENT"]=round(instrument_token_LTP[instrument_first_position],1)
	position_token_LTP_LAST[instrument_second_position]["CURRENT"]=round(instrument_token_LTP[instrument_second_position],1)

	print(position_token_LTP_FIRST)
	print(position_token_LTP_LAST)


			#writing the unrealised profits and losses code to satisfy the conditional algorithm down-----------------------------------------------------

	unrealised_first_position=(position_token_LTP_FIRST[instrument_first_position]["SELL"]-position_token_LTP_FIRST[instrument_first_position]["CURRENT"])*Quantity
	unrealised_second_position=(position_token_LTP_LAST[instrument_second_position]["SELL"]-position_token_LTP_LAST[instrument_second_position]["CURRENT"])*Quantity

	print(int(unrealised_first_position),int(unrealised_second_position))

			#spliting the instrument_token_LTP into  CE and PE lists---------------------------------------------------------------------------------------

	instrument_token_LTP_CE_check={}
	instrument_token_LTP_PE_check={}


	n=0
	for key, value in instrument_token_LTP.items():
		if n%2==0:
			instrument_token_LTP_CE_check.update({key:value})
			n+=1
		else:
			instrument_token_LTP_PE_check.update({key:value})
			n+=1

 #************************************************* IMP CODE TO PUT BUYING/SELLING ORDERS**********************************************************************************

 			##Moving down the calls-------------------------------------------------------------------------------------------------------------------------

	if unrealised_first_position<unrealised_second_position:
		Closest_instrument_value=min(instrument_token_LTP_CE_check, key=lambda y:abs(float(instrument_token_LTP_CE_check[y])-instrument_token_LTP[instrument_first_position]))
		if Closest_instrument_value != instrument_second_position and Ticker_instruement_dict[Closest_instrument_value][-7:-2] < Ticker_instruement_dict[instrument_second_position][-7:-2] and (instrument_token_LTP[instrument_first_position]-instrument_token_LTP_CE_check[Closest_instrument_value])>min(instrument_token_LTP[instrument_first_position]/4,6):
			buying_back = get_key(instrument_second_position)
			selling_lot = get_key(Closest_instrument_value)
			print(selling_lot,buying_back)
			ApplyOrders(buying_back,selling_lot,Quantity)
			del position_token_LTP_LAST[instrument_second_position]
			instrument_second_position=Closest_instrument_value
			position_token_LTP_LAST[instrument_second_position] = {"SELL": instrument_token_LTP_CE_check[Closest_instrument_value], "CURRENT": instrument_token_LTP_CE_check[Closest_instrument_value],"TRADINGSYMBOL":Ticker_instruement_dict[Closest_instrument_value]}

			##Moving up the puts ----------------------------------------------------------------------------------------------------------------------------
		
	elif unrealised_first_position>unrealised_second_position:
		Closest_instrument_value=min(instrument_token_LTP_PE_check, key=lambda y:abs(float(instrument_token_LTP_PE_check[y])-instrument_token_LTP[instrument_second_position]))
		if Closest_instrument_value!=instrument_first_position and Ticker_instruement_dict[Closest_instrument_value][-7:-2] > Ticker_instruement_dict[instrument_first_position][-7:-2] and  (instrument_token_LTP[instrument_second_position]-instrument_token_LTP_PE_check[Closest_instrument_value])>min(instrument_token_LTP[instrument_second_position]/4,6):
	 		buying_back = get_key(instrument_first_position)
	 		selling_lot = get_key(Closest_instrument_value)
	 		print(selling_lot,buying_back)
	 		ApplyOrders(buying_back,selling_lot,Quantity)
	 		del position_token_LTP_FIRST[instrument_first_position]
	 		instrument_first_position=Closest_instrument_value
	 		position_token_LTP_FIRST[instrument_first_position] = {"SELL": instrument_token_LTP_PE_check[Closest_instrument_value], "CURRENT": instrument_token_LTP_PE_check[Closest_instrument_value],"TRADINGSYMBOL":Ticker_instruement_dict[Closest_instrument_value]}



# #************************************************* IMP CODE TO PUT BUYING/SELLING ORDERS*************************************************###		

def on_connect(ws, response):
    ws.subscribe(instrument_token)
    ws.set_mode(ws.MODE_FULL,instrument_token )
    

kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.connect()