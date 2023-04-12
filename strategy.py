from data import *

total = []
total_percent = []
balance = 50

def strategy(symbol, client, switch = False):

    global total, total_percent, balance

    while switch == False:
        
        df = get_data(symbol, client)
        last_price = df['Close'][-2]
        info_qty = float(client.get_symbol_info(symbol)['filters'][2]['stepSize'])
        info_price = float(client.get_symbol_info(symbol)['filters'][0]['tickSize'])
        qty = round_step_size(float(20 / last_price), info_qty)
        price = round_step_size(float(qty * last_price), info_price)

        Calculation(df)
	
        # rsi = round(df.rsi.iloc[-2], 2)
        # ema41 = round_step_size(df.ema41.iloc[-2], info_price)
        # ema99 = round_step_size(df.ema99.iloc[-2], info_price)
        ema200 = round_step_size(df.ema200.iloc[-2], info_price)
        engulf = df.engulf.iloc[-2]

        buy_price = price
        stop_lose = df['Low'][-2]
        profit_percent = round_step_size(float(last_price - stop_lose) * 0.5, info_price)
        take_profit = round_step_size(float(last_price + profit_percent), info_price)

        print(symbol)
        print(engulf)
        print(ema200)
        
        condition1 = last_price > ema200
        condition2 = engulf==100

        schedule.run_pending()

        if condition1 and condition2:
                
            # client.order_market_buy(
                # symbol=symbol,
                # quantity=qty)
            
            # trades = float(client.get_my_trades(symbol=symbol)[-1]['commission'])
            # price = float(trades[-1]['quoteQty'])
            # quantity = float(trades[-1]['qty'])
            # last = float(trades[-1]['price'])
            switch = True
            qty_fee = round_step_size(float(qty * 0.001), info_qty)
            qty_after_fee = round_step_size(float(qty - qty_fee), info_qty) 
            balance -= price
            balance = round(balance, 2)
            # balance = round(float(client.get_asset_balance(asset='USDT')['free'])-0.01, 2)

            telegram_send.send(messages=[f"I Just Bought {qty_after_fee}\nFrom {symbol}\nFor The Price {price}\n\nQuantity before fee: {qty}\nLast price: {last_price}\nTake profit: {take_profit}\nStop lose: {stop_lose}"])

            while switch == True:

                df = get_data(symbol, client)
                last_price = df['Close'][-2]
                price_fee = round_step_size(float(qty*last_price) * 0.001, info_price)
                price_after_fee = round_step_size(float(last_price - price_fee), info_price)
                price = round_step_size(float(qty*price_after_fee), info_price)
                
                Calculation(df)
                        
                # rsi = round(df.rsi.iloc[-2], 2)
                # ema41 = round_step_size(df.ema41.iloc[-2], info_price)
                # ema99 = round_step_size(df.ema99.iloc[-2], info_price)
                ema200 = round_step_size(df.ema200.iloc[-2], info_price)
                engulf = df.engulf.iloc[-2]

                condition3 = last_price >= take_profit
                condition4 = last_price <= stop_lose

                schedule.run_pending()

                if condition3 or condition4:
                    
                    # client.order_market_sell(
                    #     symbol=symbol,
                    #     quantity=qty)

                    # trades = client.get_my_trades(symbol=symbol)
                    # price = float(trades[-1]['quoteQty'])
                    # quantity = float(trades[-1]['qty'])
                    # last = float(trades[-1]['price'])
                    balance += price
                    balance = round(balance, 2)
                    profits_percent = round(((price - buy_price)/buy_price)*100, 2)
                    profits = round(price - buy_price, 2)
                    switch = False
                    # balance = round(float(client.get_asset_balance(asset='USDT')['free'])-0.01, 2)
                    
                    total.append(profits)
                    total_percent.append(profits_percent)

                    telegram_send.send(messages=[f"I Just Sold {qty}\nFrom {symbol}\nFor The price {price}\n\nLast price: {last_price}\nPrice after fee: {price_after_fee}\nProfit: {profits_percent}%"])

                    return total, total_percent, balance

        else:
            break

def counter():
            global total, total_percent, balance

            # client = Client(api_key, api_secret, {"verify": True, "timeout": 50000})
            # balance = round(float(client.get_asset_balance(asset='USDT')['free'])-0.01, 2)
            profit_percent = round(float(sum(total_percent)), 2)
            profit = round(float(sum(total)), 2)
            date = datetime.datetime.now().strftime("%x")
            
            with open('/root/BinanceBot/portfolio.txt', 'a') as f:
                f.write(f'Date {date}\nTrades {len(total)}\nProfits {profit}USDT\nProfit Percent {profit_percent}%\n')
        
            telegram_send.send(messages=[f'Date {date}\nTrades {len(total)}\nProfits {profit}USDT\nProfit Percent {profit_percent}%\nCurrent Balance {balance}USDT\n'])

            total = []
            total_percent = []