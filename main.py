import tradingview_paper
import time
import sys

tvp = tradingview_paper
initializing_no_of_times = 0
number_of_times_browser_started = 0
amount = 100 # Dollars


def trade_up_or_down(range_btw_ema_vwap):
    UP_DOWN = 0
    for i in range(0, 21):
        print('\n\nT - ',20 - i)

        EMA = tvp.current_ema()
        VWAP = tvp.current_vwap()

        if EMA + range_btw_ema_vwap < VWAP:
            UP_DOWN -=  1
            print(UP_DOWN)

        elif EMA > VWAP + range_btw_ema_vwap:
            UP_DOWN += 1
            print(UP_DOWN)

        tvp.timmer(0.9)

def price_gained_or_not(buy_or_sell):
    while 1:
        cp = tvp.current_price()

        try:
            price_atleast = tvp.take_price_for_next_cycle()

        except:
            if buy_or_sell == 'NONE-NONE':
                print('No bit left, ready to trade')
                break
        
        if buy_or_sell == 'buy':
            if cp + 20 >= price_atleast:
                break
        
        elif buy_or_sell == 'sell':
            if cp - 20 <= price_atleast:
                break

        tvp.timmer(0.6)

def rsi_range(sell_buy, profit, gap, amount, lower_rsi, higher_rsi, cp_gap):
    for i in range(0, 6):
        RSI = tvp.current_rsi()

        if RSI > 0 and RSI < 33 and sell_buy == 'buy':
            if i >=4:
                safe_game_play(gap, amount, lower_rsi, higher_rsi, cp_gap)
            else:    
                tvp.buy_or_sell_stock_play_safe(amount, profit, 'buy')
                price_gained_or_not('buy')
            
        elif RSI > 67 and RSI < 100 and sell_buy == 'sell':
            if i >=4:
                safe_game_play(gap, amount, lower_rsi, higher_rsi, cp_gap)
            else:    
                tvp.buy_or_sell_stock_play_safe(amount, profit, 'sell')
                price_gained_or_not('sell')

        print('\n')
        tvp.timmer(0.6)

def safe_game_play(gap, amount, lower_rsi, higher_rsi, cp_gap):
    while 1:
        EMA = tvp.current_ema()
        VWAP = tvp.current_vwap()

        if EMA - VWAP > gap:

            print('Selling')
            profit = tvp.profit_for_investment(amount, tvp.current_price() + cp_gap)

            print('Profit :',profit)
            rsi_range('sell', profit, gap, amount, lower_rsi, higher_rsi, cp_gap)

        elif VWAP - EMA > gap:

            print('Buying')
            profit = tvp.profit_for_investment(amount, tvp.current_price() + cp_gap)

            print('Profit :',profit)
            rsi_range('buy', profit, gap, amount, lower_rsi, higher_rsi, cp_gap)

        tvp.timmer(0.6)

def safe_game_play_initializing(number_of_times_browser_started, amount):
    gap = int(input('Enter gap between VWAP and 9EMA ( Preffered Between 800-1000) : '))
    lower_rsi = int(input('Enter lower RSI ( Preffered Between 30-35 ) : '))
    higher_rsi = int(input('Enter higher RSI ( Preffered Between 66-70 ) : '))
    cp_gap = int(input('Enter CP-SP gap ( Preffered Between 700 - 1200 ) : '))

    tvp.start_browser(number_of_times_browser_started)
    price_gained_or_not('NONE-NONE')
    safe_game_play(gap, amount, lower_rsi, higher_rsi, cp_gap)

def hard_game_play_initializing():
    # tvp.start_browser(number_of_times_browser_started)

    # for i in range(0, 20):
    #     up_down = trade_up_or_down(150)

    #     profit = tvp.profit_for_investment(amount, tvp.current_price() + 700)

    #     if up_down >= 17:
    #         rsi_range('buy', profit)

    #     else:
    #         rsi_range('sell', profit)
    print('Not ready')

def initializing(initializing_no_of_times, number_of_times_browser_started, amount):
    initializing_no_of_times = initializing_no_of_times + 1
    try:
        # last_weeks_highest_avg = tvp.last_weeks_hihgest_average()
        # last_weeks_lowest_avg = tvp.last_weeks_lowest_average()
        last_weeks_hig_low_avg = tvp.last_weeks_hig_low_average()
        print('Last Weeks High-Low Avg :',last_weeks_hig_low_avg)

        # todays_highest = tvp.todays_highest()
        # todays_lowest = tvp.todays_lowest()
        todays_high_low_avg = tvp.todays_hig_low_average()
        print('Todays High-Low Avg :',todays_high_low_avg)

        if todays_high_low_avg - 3000 < last_weeks_hig_low_avg and todays_high_low_avg + 3000 > last_weeks_hig_low_avg:
            print('Entered Safe Game Play')
            safe_game_play_initializing(number_of_times_browser_started, amount)

        else:
            print('Not so safe game play | sell and buy') 
    
    except:
        print("\n\nYahoo's data is revising, Will work again in next 5 minutes.\n")

        for i in range(101):
            sys.stdout.write('\r')
            sys.stdout.write("[%-100s] %d%%" % ('='*i, 1*i))
            sys.stdout.flush()
            time.sleep(3)

        print('\n')

        if initializing_no_of_times == 11: # It loop for 10 times
            print("Somethings's Wrong.")
            tvp.send_message_normal('Initializing', 'Somethings wrong with the data\nPlease check this', 'NONE-NONE')
        
        else:
            initializing(initializing_no_of_times)

if __name__ == '__main__':
    initializing(initializing_no_of_times,number_of_times_browser_started, amount)

    

    
