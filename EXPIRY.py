import Credentials
import csv
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
from pprint import pprint
import logging
import pandas as pd
import datetime
import pdb
import json
from datetime import datetime, timedelta

# *******************************************************SETTING UP THE CONNECTION*******************************************DO NOT TOUCH*********************
# initialisation
logging.basicConfig(level=logging.DEBUG)
kite = KiteConnect(api_key=Credentials.api_key)
kws = KiteTicker(Credentials.api_key, Credentials.access_token)
kite.set_access_token(Credentials.access_token)

# *******************************************************SETTING UP THE CONNECTION*******************************************DO NOT TOUCH*********************


# *******************************NEW CODE TO GET CURRENT EXPIRY DATE BY IT"S OWN *****************************************************************************

Weekdays = {'Monday': '3', 'Tuesday': '2',
            'Wednesday': '1', 'Thursday': '0', 'Friday': '6'}
currentDateTime = datetime.now()
Time = currentDateTime.strftime("%H:%M:%S")
Day = currentDateTime.strftime("%A")
ExpiryDate = (currentDateTime +
              timedelta(days=int(Weekdays[Day]))).strftime("%#m/%#d/%Y")
pprint('Expiry Date: ' + ExpiryDate + ' ' + Time + ' ' + Day)

# *******************************NEW CODE TO GET CURRENT EXPIRY DATE BY IT"S OWN ******************************************************************************


# *******************************GETTING POSITIONS AND CREATING FEW LISTS *************************************************************************************

# -------------------------------Get position of orders--------------------------------------------------------------------------------------------------------

position = kite.positions()
all_positions = position["net"]

# -------------------------------Defining variables------------------------------------------------------------------------------------------------------------
Position_tokens = []
Positions_symbol = []
Positions_InstrumentTokens = []
Quantity = []

# -------------------------------Getting the positions in terminal and all the related values------------------------------------------------------------------

for n in all_positions:
    if n["product"] == "NRML" and n["sell_price"] > 0 and n["quantity"] < 0:
        # position_tokens[n["instrument_token"]]={"SELL":n["average_price"],"CURRENT":0,"Quantity":abs(n["quantity"]),"TRADINGSYMBOL":n["tradingsymbol"]}
        token = {n["instrument_token"]: {"SELL": round(n["average_price"], 1), "CURRENT": round(
            0, 1), "QUANTITY": abs(n["quantity"]), "TRADINGSYMBOL": n["tradingsymbol"]}}
        Position_tokens.append(token)
        Positions_symbol.append(n["tradingsymbol"])
        Positions_InstrumentTokens.append(n["instrument_token"])
        Quantity.append(n["quantity"])
        PRODUCT_MIS_NRML = n["product"]
pprint(Position_tokens)
pprint(Positions_symbol)

# Assigning Format of the first and last value orders("SELL":n["average_price"],"CURRENT":0,"Quantity":abs(n["quantity"]),"TRADINGSYMBOL":n["tradingsymbol"])--

position_token_LTP_FIRST = Position_tokens[0]
position_token_LTP_LAST = Position_tokens[1]

# -------------------------------Tradingsymbol of the first and last value orders------------------------------------------------------------------------------

START = Positions_symbol[0]
END = Positions_symbol[1]

# -------------------------------Instrument token of the first and last value orders---------------------------------------------------------------------------

instrument_first_position = Positions_InstrumentTokens[0]
instrument_second_position = Positions_InstrumentTokens[1]

# -------------------------------Getting the strike prices range-----------------------------------------------------------------------------------------------

Start_value = int(START[-7:-2]) - int(150)
End_value = int(END[-7:-2]) + int(150)

# -------------------------------StrikePriceList to develop TradingSymbolList ---------------------------------------------------------------------------------

StrikePriceList = []
StrikePriceList.append(int(Start_value))
Factor = (int(End_value)-int(Start_value))/35
n = 1
while n < Factor:
    StrikePriceList.append(int(Start_value)+50*n)
    n += 1
print(StrikePriceList)

# -------------------------------TradingSymbolList for all the strike Prices-----------------------------------------------------------------------------------

TradingSymbolList = []
for n in StrikePriceList:
    CE_Values = END[0:10]+str(n) + END[-2:]
    PE_Values = START[0:10]+str(n)+START[-2:]
    TradingSymbolList.append(CE_Values)
    TradingSymbolList.append(PE_Values)
print(TradingSymbolList)
# *******************************GETTING POSITIONS AND CREATING FEW LISTS **************************************************************************************


# *******************************READING FILE AND CREATING FEW LISTS *******************************************************************************************

# -------------------------------InstrumentTokenList by Reading the Instrument2022.txt File --------------------------------------------------------------------

instrument_token_list = []
instrument_token_list1 = []
instrument_token1 = []
InstrumentTokenList = []


with open('Instrument2022.txt', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for n in csv_reader:
        instrument_token_list.append(n[0])

for n in instrument_token_list:
    list = n.split("	")
    instrument_token_list1.append(list)

for n in TradingSymbolList:
    for k in instrument_token_list1:
        if n == k[2] and ExpiryDate == str(k[5]):
            instrument_token1.append(k[0])

for n in instrument_token1:
    InstrumentTokenList.append(int(n))

print(InstrumentTokenList)

# ------------------------------TradingSymbolList_InstrumentTokenList_dict  with TradingSymbol and IntrumentToken for ORDER PUTTING FUNCTION---------------------

TradingSymbolList_InstrumentTokenList_dict = dict(
    zip(TradingSymbolList, InstrumentTokenList))

# ------------------------------InstrumentTokenList_TradingSymbolList_dict  with IntrumentToken and TradingSymbol for ORDER PUTTING FUNCTION---------------------
# ------------------------------This is being used in if conditions for the difference between the values while executing for our strategy-----------------------

InstrumentTokenList_TradingSymbolList_dict = dict(
    zip(InstrumentTokenList, TradingSymbolList))

# *******************************READING FILE AND CREATING FEW LISTS ********************************************************************************************


# *******************************CREATING BUYING and SELLING FUNC TO PLACE ORDERS *******************************************************************************

Quantity = abs(Quantity[0])


def ApplyOrders(buying_back, selling_lot, Quantity):
    print(buying_back)
    print(selling_lot)
    kite.place_order(tradingsymbol=buying_back,
                     exchange=kite.EXCHANGE_NFO,
                     variety=kite.VARIETY_REGULAR,
                     transaction_type=kite.TRANSACTION_TYPE_BUY,
                     quantity=Quantity,
                     order_type=kite.ORDER_TYPE_MARKET,
                     product=kite.PRODUCT_NRML)
    kite.place_order(tradingsymbol=selling_lot,
                     exchange=kite.EXCHANGE_NFO,
                     variety=kite.VARIETY_REGULAR,
                     transaction_type=kite.TRANSACTION_TYPE_SELL,
                     quantity=Quantity,
                     order_type=kite.ORDER_TYPE_MARKET,
                     product=kite.PRODUCT_NRML)


# *******************************CREATING BUYING and SELLING FUNC TO PLACE ORDERS *******************************************************************************
# --------------------------------Getting the Key from TradingSymbolList_InstrumentTokenList_dict and that's TradingSymbol ---------------------------------------


def get_key(val):
    for key, value in TradingSymbolList_InstrumentTokenList_dict.items():
        if val == value:
            return key

# *******************************SETTING UP LIVE ALGORITHM FOR MANAGING STRANGGLE  ******************************************************************************

# ------------------------------- InstrumentToken_LTPList dict of intrumentToken and LTP with LTP -1 for time being to be used inside on_ticks function-----------


InstrumentToken_LTPList = dict.fromkeys(InstrumentTokenList, "-1")


def on_ticks(ws, ticks):
    # ---------------------------- using the first and second position variables inside on_ticks------------------------------------------------------------------
    global instrument_first_position
    global instrument_second_position

    for token in ticks:
        token_value = token["instrument_token"]
        ltp = token['last_price']
        InstrumentToken_LTPList.update({token_value: ltp})
    # print(InstrumentToken_LTPList)

    # ---------------------------- updating the current LTP value of instrument which we have selled to ease down the computations------------------------------------

    position_token_LTP_FIRST[instrument_first_position]["CURRENT"] = round(
        InstrumentToken_LTPList[instrument_first_position], 1)
    position_token_LTP_LAST[instrument_second_position]["CURRENT"] = round(
        InstrumentToken_LTPList[instrument_second_position], 1)

    print(position_token_LTP_FIRST)
    print(position_token_LTP_LAST)

    # -----------------------------Writing the unrealised profits and losses code to satisfy the conditional algorithm down----------------------------------------

    unrealised_first_position = (position_token_LTP_FIRST[instrument_first_position]
                                 ["SELL"]-position_token_LTP_FIRST[instrument_first_position]["CURRENT"])*Quantity
    unrealised_second_position = (position_token_LTP_LAST[instrument_second_position]
                                  ["SELL"]-position_token_LTP_LAST[instrument_second_position]["CURRENT"])*Quantity

    print(int(unrealised_first_position), int(unrealised_second_position))

    # -----------------------------Spliting the InstrumentToken_LTPList into CE and PE lists just to check Closest_instrument_value-----------------------------------------------------------------------

    InstrumentToken_LTPList_CE_check = {}
    InstrumentToken_LTPList_PE_check = {}

    n = 0
    for key, value in InstrumentToken_LTPList.items():
        if n % 2 == 0:
            InstrumentToken_LTPList_CE_check.update({key: value})
            n += 1
        else:
            InstrumentToken_LTPList_PE_check.update({key: value})
            n += 1
    # print(InstrumentToken_LTPList_CE_check)
    # print(InstrumentToken_LTPList_PE_check)

    # ****************************IMP CODE TO PUT BUYING/SELLING ORDERS*****************************************************************************************

    # ----------------------------Moving down the calls---------------------------------------------------------------------------------------------------------

    if unrealised_first_position < unrealised_second_position and unrealised_second_position > 0:
        # ----------------- ------Closest_instrument_value gives the token value and not the tradingSymbol------------------------------------------------------
        Closest_instrument_value = min(InstrumentToken_LTPList_CE_check, key=lambda y: abs(
            float(InstrumentToken_LTPList_CE_check[y])-InstrumentToken_LTPList[instrument_first_position]))

        pprint("Nearing call Down" + ' ' + get_key(Closest_instrument_value) + ' ' +
               str(round(InstrumentToken_LTPList[instrument_first_position]-InstrumentToken_LTPList[Closest_instrument_value], 2)) + ' ' + str(round(InstrumentToken_LTPList[Closest_instrument_value]-InstrumentToken_LTPList[instrument_second_position], 2)/2.15))
        if (Closest_instrument_value != instrument_second_position and InstrumentTokenList_TradingSymbolList_dict[Closest_instrument_value][-7:-2] < InstrumentTokenList_TradingSymbolList_dict[instrument_second_position][-7:-2]) and ((InstrumentToken_LTPList[instrument_first_position]-InstrumentToken_LTPList[Closest_instrument_value]) > min(InstrumentToken_LTPList[instrument_first_position]/4, (InstrumentToken_LTPList[Closest_instrument_value]-InstrumentToken_LTPList[instrument_second_position])/2.15)):
            buying_back = get_key(instrument_second_position)
            selling_lot = get_key(Closest_instrument_value)
            print(buying_back, selling_lot)
            ApplyOrders(buying_back, selling_lot, Quantity)
            del position_token_LTP_LAST[instrument_second_position]
            instrument_second_position = Closest_instrument_value
            position_token_LTP_LAST[instrument_second_position] = {"SELL": InstrumentToken_LTPList[Closest_instrument_value],
                                                                   "CURRENT": InstrumentToken_LTPList[Closest_instrument_value], "QUANTITY": Quantity, "TRADINGSYMBOL": InstrumentTokenList_TradingSymbolList_dict[Closest_instrument_value]}

    # ----------------------------Moving up the puts ----------------------------------------------------------------------------------------------------------

    elif unrealised_first_position > unrealised_second_position and unrealised_first_position > 0:
        Closest_instrument_value = min(InstrumentToken_LTPList_PE_check, key=lambda y: abs(float(
            InstrumentToken_LTPList_PE_check[y])-InstrumentToken_LTPList[instrument_second_position]))
        pprint("nearing put up" + ' ' + get_key(Closest_instrument_value) + ' ' +
               str(round(InstrumentToken_LTPList[instrument_second_position]-InstrumentToken_LTPList[Closest_instrument_value], 2)) + ' ' + str(round(InstrumentToken_LTPList[Closest_instrument_value]-InstrumentToken_LTPList[instrument_first_position], 2)/2.15))
        if (Closest_instrument_value != instrument_first_position and InstrumentTokenList_TradingSymbolList_dict[Closest_instrument_value][-7:-2] > InstrumentTokenList_TradingSymbolList_dict[instrument_first_position][-7:-2]) and ((InstrumentToken_LTPList[instrument_second_position]-InstrumentToken_LTPList[Closest_instrument_value]) > min(InstrumentToken_LTPList[instrument_second_position]/4, (InstrumentToken_LTPList[Closest_instrument_value]-InstrumentToken_LTPList[instrument_first_position])/2.15)):
            buying_back = get_key(instrument_first_position)
            selling_lot = get_key(Closest_instrument_value)
            print(buying_back, selling_lot)
            ApplyOrders(buying_back, selling_lot, Quantity)
            del position_token_LTP_FIRST[instrument_first_position]
            instrument_first_position = Closest_instrument_value
            position_token_LTP_FIRST[instrument_first_position] = {"SELL": InstrumentToken_LTPList[Closest_instrument_value],
                                                                   "CURRENT": InstrumentToken_LTPList[Closest_instrument_value], "QUANTITY": Quantity, "TRADINGSYMBOL": InstrumentTokenList_TradingSymbolList_dict[Closest_instrument_value]}

        # ************************************************* IMP CODE TO PUT BUYING/SELLING ORDERS************************************************************************


def on_connect(ws, response):
    ws.subscribe(InstrumentTokenList)
    ws.set_mode(ws.MODE_FULL, InstrumentTokenList)


kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.connect()
