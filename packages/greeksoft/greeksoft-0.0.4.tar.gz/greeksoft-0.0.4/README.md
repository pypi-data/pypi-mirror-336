# GreekSoft API
Greeksoft API is a Python-based package that allows users to subscribe to the Greek token and retrieve the latest tick by tick data. This project helps in authenticating a user, broadcasting tokens, and placing orders in a seamless manner.

# Features Authentication: 
By passing a username, session password, and user password, the project authenticates the user.
# Token Retrieval: 
Retrieves the latest token broadcast.
# Order Placement: 
Capable of placing orders once authenticated.

# Technologies Used
Python built-in Libs & third party libs (Pandas, numpy,requests,etc.)


# What's New in Version 0.0.4

**New Feature**: Added New Feature to get the limited data of net_position by passing api.Net_Position_request().

**New Feature**: Added New Feature to get the detailed data of all net_position by passing api.Net_position_Detailed().

**New Feature**: Added New Feature to check the status of all traded orders by passing api.Order_Trade_status('gorderid') by passing greek order id as in string.

**New Feature**: Added New Feature to check all Pending Order if Booked order is being in pending passing api.all_Pending_order()

**New Feature**: Added New Feature to Modify Order if Booked order is being in pending passing api.all_Pending_order() and api.modify_order(price,qty,ordtype,gorderid) as price,qty,gorderid id should be passed in String and ordtype must be in string.

**New Feature**: Added New Feature to cancel order if booked order is being pending, just by passing api.cancel_order('ord_id') as ord_id must be greek order id and to be passed as in String.

**New Feature**: Added New Feature to get the data of all rejected order by exchange, disable id or by exceed limit, using api.Orderbook_Rejected()

**New Feature**: Added New Feature to get the list of every order booked and got traded also with pending order with all strategy wise, using api.Orderbook_All()

**New Feature**: Added New Feature to get the list of every order booked and got traded,with strategy wise, using api.Orderbook_Traded()

```
pip install greeksoft
```

Usage
Once installed, you can use the project by importing the Greek_API from the greek_api_client package. Below is an example of how to use the API:

```
from greeksoft import GreekAPI

username="username" # String Format

session_pwd="session_pwd"  #String Format

user_pwd="user_pwd" #String Format

procli="procli" # for client id procli="2", retail id procli='1'

ac_no='ac_no' # if retail id pass account number in String Format. 

api = Greek_API(username,session_pwd,user_pwd,procli,ac_no) #to authenticate the creadentials passed.

token_no='102000000' # string format

# Authenticate and fetch the latest token

token = api.token_broadcast('token_no','asset_type') # token_no in 'String', asset_type='option' or 'future' or 'equity' in string format.

# token=token['data.token'][0] <-- get token no

# symbol=token['data.symbol'][0] <-- get symbol name of token passed

# time=token['data.ltt'][0] <-- provide the time

# strike=token['data.strikeprice'][0] <-- get Strike 

# option_type=token['data.optiontype'][0] <-- get Option type CE or PE

# instrument=token['data.instrument'][0] <-- get instrument type FUTSTK,OPTSTK...

# bid_price=token[data.bid][0] <-- get bid price of token passed 

# ask_price=token['data.ask'][0] <-- get ask price of token passed


# Subscribe with the Greek Token and pass it in list eg:token_list=['','',...] into the declared variable. 

token_list=['102000000','102000000',...] # Only pass Greek Token.

req_data='' For passing empty string we will get only token,symbol,last traded price, last traded time.

req_data='depth' For passing depth as string we will get only token, symbol,depth inplace of last traded price, last traded time.

req_data='ask/bid' For passing ask/bid as string we will get token, symbol,ask price and its bid price, last traded time.req_data

req_data='allresp' For passing allresp as string we will get token.symbol,all data of traded at the respective time and its last traded time.

for data in api.get_apollo_resp(token_list): # To get response of tokens passed of list using loop.
    print(data)

# Place order passing required paramets, # token_no='102000000', symbol="RELIANCE", qty="minimum_lot" for respective token,

# price= value get from bid/ask price from token broadcast against respective token in strictly in string format,

#buysell= if buy then pass 1 and for sell 2 in integer format,

ordtype=1, trigprice=0, strategyname="example" strategy name will be anything as per userinput.

var_response=api.place_order(tokenno,symbol,lot,qty,price,buysell,ordtype,trigprice,strategyname) # pass the required parameters

print(var_response) # acknowledge the response get from place order function.

**Unsubscribe Token**
api.unsubscribe_token(token) # Token in string--MANDATORY

**Close connection**
api.close_connection() # to terminate all sessions

**NetPosition as per StrategyWise**

net_position_strategywise=api.Net_Position_Details_strategywise() # to get the net position of Greek ID as per strategy wise
print(net_position)

**NetPosition request**

net_position_request=api.Net_Position_request() # to get the limited data of net position of Greek ID.strategy

**NetPosition Detailed**

net_position_detailed=api.Net_position_Detailed() # to get the detailed data of the net position of Greek ID

**Order Traded Status**

order_traded_status=api.Order_Trade_status('gorderid') # to get the status of booked order status of Greekorder_Id passed as string.

**Pending Order**

pending_order=api.all_pending_order() # by calling this function we will get all pending order status as while using this function no parameters required to be passed.

**Cancel Order**

cancel_order=api.cancel_order(ord_id) # just passing the greek orderid as string and to cancel the pending order.

**Modify Order**

modify_order=api.modify_order(price,lot,qty,ordtype,gorderid) # to modify the pending order by its latest ask/bid price as in string ,in lot will be the value of multiple of minimum_lot in string,its quantity in string, ordtype in interger and mandatory part gorderid as greek order id in string.

**Rejected Order**

rejected_order=api.api.Orderbook_Rejected() # to get list of all rejected order.

**Orderbook All**

orderbook_all=api.Orderbook_All() # to get the list of all placed order,pending_order ,with all strategy wise.

**Orderbook Traded**

orderbook_traded=api.Orderbook_Traded() # to get the list of all placed and confirmed Booked orders data with all strategy wise.

```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.




