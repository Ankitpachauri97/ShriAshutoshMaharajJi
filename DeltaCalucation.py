from BankNiftyCode import ExpiryDate
import math
from numpy import random
import datetime
import time

flag=1
def bns(Nifty_50_LTP,India_Vix_LTP,StrikePrice):
    spot = Nifty_50_LTP
    strike = StrikePrice
    expiry = ExpiryDate
    volt = India_Vix_LTP;
    int_rate = 7;
    div_yld = 0;
	
    date_now = datetime.now().date();
    seconds = math.floor((ExpiryDate - (date_now))/1000),
    minutes = math.floor(seconds/60),
    hours = math.floor(minutes/60),
    delta_t = (math.floor(hours/24))/365.0;

    volt = volt/100;
    int_rate = int_rate/100;
    if(flag==1):
        d1 = (math.log(spot/strike) + (int_rate + math.pow(volt,2)/2) * delta_t) / (volt*math.sqrt(delta_t)),
        d2 = (math.log(spot/strike) + (int_rate - math.pow(volt,2)/2) * delta_t) / (volt*math.sqrt(delta_t));

        fv_strike = (strike)*math.exp(-1*int_rate*delta_t);

        
        distribution = random.normal(size=(0, 1))

        
        call_premium = spot * distribution.cdf(d1) - fv_strike * distribution.cdf(d2),
        put_premium = fv_strike * distribution.cdf(-1*d2) - spot * distribution.cdf(-1*d1);

        
        call_delta = distribution.cdf(d1),
        put_delta = call_delta-1;

        call_gamma = distribution.pdf(d1)/(spot*volt*math.sqrt(delta_t)),
        put_gamma = call_gamma; 

        call_vega = spot*distribution.pdf(d1)*math.sqrt(delta_t)/100,
        put_vega = call_vega;

        call_theta = (-1*spot*distribution.pdf(d1)*volt/(2*math.sqrt(delta_t)) - int_rate*fv_strike*distribution.cdf(d2))/365,
        put_theta = (-1*spot*distribution.pdf(d1)*volt/(2*math.sqrt(delta_t)) + int_rate*fv_strike*distribution.cdf(-1*d2))/365;

        call_rho = fv_strike*delta_t*distribution.cdf(d2)/100,
        put_rho = -1*fv_strike*delta_t*distribution.cdf(-1*d2)/100;
        
        bns_results = {
            "call_option_prem_value": call_premium.toFixed(2),
            "put_option_prem_value": put_premium.toFixed(2),
            "call_option_delta_value": call_delta.toFixed(3),
            "put_option_delta_value": put_delta.toFixed(3),
            "option_gamma_value": call_gamma.toFixed(4),
            "call_option_theta_value": call_theta.toFixed(3),
            "put_option_theta_value": put_theta.toFixed(3),
            "call_option_rho_value": call_rho.toFixed(3),
            "put_option_rho_value": put_rho.toFixed(3),
            "option_vega_value": call_vega.toFixed(3)
        } 
