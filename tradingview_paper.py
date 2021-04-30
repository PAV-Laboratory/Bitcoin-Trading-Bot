from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from discord_webhook import DiscordWebhook, DiscordEmbed
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import subprocess
import requests
import random
import time
import sys
import os

options = Options()
options.add_argument("start-maximized")
options.add_argument("--start-maximized")

options.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.notifications": 1,
    "profile.default_content_setting_values.media_stream_camera": 0,
    "profile.default_content_setting_values.media_stream_mic": 0,
    "profile.default_content_setting_values.geolocation": 0
  })

driver = None
URL = "https://www.tradingview.com/"

username = 'Enter your username'
password = 'Enter your password'

webhookUrl = 'Enter your discord webhook URL'

number_of_times_browser_started = 0

def findingStockPrice():
    request = requests.get('https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD&.tsrc=fin-srch')
    content = request.content
    soup = BeautifulSoup(content, 'html.parser')

    stock_name = 'Bitcoin'
    stock_price = soup.find('span', attrs={'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).get_text()
    stock_price_int = int(stock_price[0] + stock_price[1] + stock_price[3] + stock_price[4] + stock_price[5])

    return stock_price_int

def send_message_normal(status, body, next_task):
    webhook = DiscordWebhook(url = webhookUrl, username = "BITCOIN")

    embed = DiscordEmbed(
                            title = status,
                            description = body,
                            color = 0x546e7a
    )

    embed.set_author(
                        name = "Tanishq Singh",
                        icon_url = "https://avatars.githubusercontent.com/u/76192403?s=460&u=b8fade49d1999d6a19e14326c31ee24f79b5d6c4&v=4",
    )

    if next_task != 'NONE-NONE':
        embed.set_footer(text = next_task)

    embed.set_timestamp()
    webhook.add_embed(embed)

    response = webhook.execute()

def send_message_stock_status(status, buyed_price, selled_price, profit, balence, nextTask):
    webhook = DiscordWebhook(url = webhookUrl, username = "BITCOIN")

    body = 'Purchasing Price   :   ' + buyed_price + '\nTrading Price         :   '+ selled_price + '\nProfit   :   ' + profit + '\nBalence   :   ' + balence

    embed = DiscordEmbed(
                            title = status,
                            description = body,
                            color = 0x546e7a
    )

    embed.set_author(
                        name = "Tanishq Singh",
                        icon_url = "https://avatars.githubusercontent.com/u/76192403?s=460&u=b8fade49d1999d6a19e14326c31ee24f79b5d6c4&v=4",
    )

    embed.set_footer(text = nextTask)
    embed.set_timestamp()
    webhook.add_embed(embed)

    response = webhook.execute()

def current_price():
    global driver

    try:
        price = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[8]/div[1]/div/div/div[1]/div[2]/div/div[2]/div[2]/div"))
        )

    finally:
        print("Price :",price.text)

    stock_price = price.text

    stock_price_int = int(stock_price[0] + stock_price[1] + stock_price[2] + stock_price[3] + stock_price[4])

    return stock_price_int

def current_ema():
    global driver

    class_name = driver.find_elements_by_class_name('valueValue-2KhwsEwE')
    l = 0
    for i in class_name:
        if i.text == None or i.text == '':
            if l == 6:
                k = 0
                class_name_1 = driver.find_elements_by_class_name('valueValue-2KhwsEwE')
                for j in class_name_1:
                    if k == 8:
                        c_ema = j.text
                        c_ema_int = int(c_ema[0] + c_ema[1] + c_ema[2] + c_ema[3] + c_ema[4])
                        print('\nEMA : ',c_ema_int)
                        return c_ema_int

                    k = k + 1

        elif l == 7:
            c_ema = i.text
            c_ema_int = int(c_ema[0] + c_ema[1] + c_ema[2] + c_ema[3] + c_ema[4])
            print(c_ema_int)
            return c_ema_int

        l = l + 1

def current_vwap():
    global driver

    class_name1 = driver.find_elements_by_class_name('valueValue-2KhwsEwE')
    l = 0
    for i in class_name1:
        if i.text == None or i.text == '':
            if l == 6:
                k = 0
                class_name2 = driver.find_elements_by_class_name('valueValue-2KhwsEwE')
                for j in class_name2:
                    if k == 9:
                        c_vwap = j.text
                        c_vwap_int = int(c_vwap[0] + c_vwap[1] + c_vwap[2] + c_vwap[3] + c_vwap[4])
                        print('VWAP :',c_vwap_int)
                        return c_vwap_int

                    k = k + 1

        elif l == 8:
            c_vwap = i.text
            c_vwap_int = int(c_vwap[0] + c_vwap[1] + c_vwap[2] + c_vwap[3] + c_vwap[4])
            print('VWAP :',c_vwap_int)
            return c_vwap_int

        l = l + 1

def current_rsi():
    global driver

    class_name4 = driver.find_elements_by_class_name('valueValue-2KhwsEwE')
    l = 0
    for i in class_name4:
        if i.text == None or i.text == '':
            if l == 6:
                k = 0
                class_name5 = driver.find_elements_by_class_name('valueValue-2KhwsEwE')
                for j in class_name5:
                    if k == 10:
                        c_rsi = j.text

                        try:
                            c_rsi_int = int(c_rsi[0] + c_rsi[1] + c_rsi[2])
                            print('RSI :',c_rsi_int)
                            return c_rsi_int

                        except:
                            c_rsi_int = int(c_rsi[0] + c_rsi[1])
                            print('RSI',c_rsi_int)
                            return c_rsi_int

                    k = k + 1

        elif l == 9:
            c_rsi = i.text

            try:
                c_rsi_int = int(c_rsi[0] + c_rsi[1] + c_rsi[2])
                print('RSI :',c_rsi_int)
                return c_rsi_int

            except:
                c_rsi_int = int(c_rsi[0] + c_rsi[1])
                print('RSI',c_rsi_int)
                return c_rsi_int

        l = l + 1

def take_price_for_next_cycle():
    global driver
    data = driver.find_elements_by_class_name('tv-am-data-table__cell--right-align')

    j = 0
    for i in data:
        if j == 8:
            take_profit = i.text
            take_profit_int = int(take_profit[0] + take_profit[1] + take_profit[3] + take_profit[4] + take_profit[5])
            print('Take Profit :',take_profit_int)
            return take_profit_int

        j +=1

def profit_for_investment(invested_money, selling_price):
    cp = current_price()
    return round((invested_money * (selling_price - cp)) / cp,2)

def selling_price_for_profit(invested_money, profit_you_want_to_make):
    cp = current_price()
    return ((cp * (profit_you_want_to_make + invested_money)) / invested_money)

def buy_or_sell_stock_play_safe(amount, profit_money, buy_or_sell):
    global driver
    # buying_button = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[1]/div[1]/div[2]/div[3]')
    # buying_button.click()

    if buy_or_sell.lower() == 'buy':
        try:
            buying_button = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[8]/div[1]/div/div/div[1]/div[2]/div/div[2]"))
            )

            buying_button.click()

        finally:
            print('Buying Button Clicked.')

    elif buy_or_sell.lower() == 'sell':
        try:
            selling_button = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[8]/div[1]/div/div/div[1]/div[2]/div/div[1]"))
            )

            selling_button.click()

        finally:
            print('Selling Button Clicked.')

    time.sleep(1)

    cp = current_price()

    quantity = round((amount / cp),4)

    print('Stocks Quantity :',quantity)

    market_button = driver.find_element_by_xpath('/html/body/div[2]/div[8]/div[1]/div/div/div[1]/div[3]/div/div[1]/div[1]')
    market_button.click()

    enter_quantity = driver.find_element_by_xpath('/html/body/div[2]/div[8]/div[1]/div/div/div[1]/div[5]/div/div[2]/div[1]/span/div/div/div/div[1]/input')
    enter_quantity.click()

    try:
        for i in range(0,5):
            enter_quantity.send_keys(Keys.BACK_SPACE)

    except:
        print('Done clearing')

    enter_quantity.send_keys(str(quantity))

    try:

        try:
            take_profit_button = driver.find_element_by_xpath('/html/body/div[2]/div[8]/div[1]/div/div/div[1]/div[5]/div/div[4]/div[1]/label/span[1]/input')
            take_profit_button.click()

        except:
            try:
                time.sleep(2)
                take_profit_button = driver.find_elements_by_class_name('input-24iGIobO')

                for i in take_profit_button:
                    i.click()

            except:
                try:
                    time.sleep(2)
                    take_profit_button_name = driver.find_element_by_xpath('/html/body/div[2]/div[8]/div[1]/div/div/div[1]/div[5]/div/div[4]/div[1]/label/span[2]/span')
                    take_profit_button_name.click()

                except:
                    try:
                        take_profit_button_span_box = driver.find_elements_by_class_name('checkboxWrapper-1bflEmD_')

                        for i in take_profit_button_span_box:
                            i.click()
                    except:
                        try:
                            print(Exception)
                        except:
                            print('Exception')


        try:
            time.sleep(1)
            enter_profit_money = driver.find_element_by_xpath('/html/body/div[2]/div[8]/div[1]/div/div/div[1]/div[5]/div/div[4]/div[2]/div[3]/div/div/div[1]/input')
            enter_profit_money.click()

        except:
            try:
                time.sleep(2)
                enter_profit_money = driver.find_element_by_xpath('/html/body/div[2]/div[8]/div[1]/div/div/div[1]/div[5]/div/div[4]/div[2]/div[3]/div/div/div[1]/input')
                enter_profit_money.click()

            except:
                time.sleep(2)
                enter_profit_money = driver.find_element_by_xpath('/html/body/div[2]/div[8]/div[1]/div/div/div[1]/div[5]/div/div[4]/div[2]/div[3]/div/div/div[1]/input')
                enter_profit_money.click()

        try:
            for i in range (1, 11):
                enter_profit_money.send_keys(Keys.BACK_SPACE)

        except:
            print('Cleared Amount')

        enter_profit_money.send_keys(str(profit_money))

        # buying_button = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[8]/div[1]/div/div/div[1]/div[6]/button'))
        # )

        # buying_button.click()

        try:
            time.sleep(1)
            buying_button = driver.find_element_by_xpath('/html/body/div[2]/div[8]/div[1]/div/div/div[1]/div[6]/button')
            buying_button.click()

        except:
            try:
                time.sleep(2)
                buying_button = driver.find_element_by_xpath('/html/body/div[2]/div[8]/div[1]/div/div/div[1]/div[6]/button')
                buying_button.click()

            except:
                time.sleep(2)
                buying_button = driver.find_element_by_class_name('buy-aNdypdnc')
                buying_button.click()

    except:
        print('Oops, Something went wrong')

    time.sleep(10)
    send_message_normal('Stocks', buy_or_sell, 'NONE-NONE')

    try:
        time.sleep(10)
        close_ads()

    except:
        print("Close Ads didn't worked")

def close_ads():

    time.sleep(10)

    for i in range(0,2):

        time.sleep(3)

        try:
            ads = driver.find_elements_by_class_name('close-button-7uy97o5_')

            for i in ads:
                i.click()
                time.sleep(1)

        except:
            try:
                ads = driver.find_elements_by_class_name('close-icon-3l9twKS_')

                for i in ads:
                    i.click()
                    time.sleep(1)

            except:
                print('No ads')

        time.sleep(2)

        try:
            ads = driver.find_elements_by_class_name('close-button-T9ne7VOm')

            for i in ads:
                i.click()
                time.sleep(1)

        except:
            try:
                ads = driver.find_elements_by_class_name('closeButton-3bbdcavh')

                for i in ads:
                    i.click()
                    time.sleep(1)

            except:
                print('No Big ads')

def connect_to_paper():
    try:
        connect_button = driver.find_element_by_xpath('/html/body/div[8]/div/div/div[2]/div/div/div[1]/div[2]/form/button')
        connect_button.click()
    except:
        connect_button = driver.find_element_by_xpath('//*[@id="overlap-manager-root"]/div/div/div[2]/div/div/div[1]/div[2]/form/button')
        connect_button.click()

def loging_status():
    try:
        connect_to_paper()

    except:
        time.sleep(1)
        print('Connecting to paper')
        loging_status()

def login(number_of_times_browser_started):
    global driver

    # login_link = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div/div/p[1]/a')
    # login_link.click()

    time.sleep(2)


    try:
        try:
            email_login = driver.find_element_by_xpath('//*[@id="overlap-manager-root"]/div/div[2]/div/div/div/div/div/div/div[1]/div[4]/div/span')
            email_login.click()

        except:
            time.sleep(2)

            email_login = driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div/div/div/div/div/div[1]/div[4]/div/span')
            email_login.click()

        time.sleep(2)

        try:
            enter_username = driver.find_element_by_id('email-signin__user-name-input__054b39cf-fdfb-4d0d-a116-4df68ef931b5')
            enter_username.click()

        except:
            try:
                enter_username = driver.find_element_by_xpath('//*[@id="email-signin__user-name-input__054b39cf-fdfb-4d0d-a116-4df68ef931b5"]')
                enter_username.click()

            except:
                enter_username = driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div/div/div/div/div/form/div[1]/div[1]/input')
                enter_username.click()

        for i in range(0,15):
            enter_username.send_keys(username[i])
            time.sleep(round(random.uniform(0.1, 0.9),3))

        time.sleep(round(random.uniform(1, 3),3))

        try:
            enter_password = driver.find_element_by_id('email-signin__password-input__054b39cf-fdfb-4d0d-a116-4df68ef931b5')
            enter_password.click()

        except:
            try:
                enter_password = driver.find_element_by_xpath('//*[@id="email-signin__password-input__054b39cf-fdfb-4d0d-a116-4df68ef931b5"]')
                enter_password.click()

            except:
                enter_password = driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div/div/div/div/div/form/div[2]/div[1]/input')
                enter_password.click()

        for i in range(0,26):
            enter_password.send_keys(password[i])
            time.sleep(round(random.uniform(0.1, 0.9),3))

        time.sleep(round(random.uniform(1, 3),3))

        try:
            submit_button = driver.find_element_by_id('email-signin__submit-button__054b39cf-fdfb-4d0d-a116-4df68ef931b5')
            submit_button.click()

        except:
            try:
                submit_button = driver.find_element_by_xpath('//*[@id="email-signin__submit-button__054b39cf-fdfb-4d0d-a116-4df68ef931b5"]')
                submit_button.click()

            except:
                submit_button = driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div/div/div/div/div/form/div[5]/div[2]/button')
                submit_button.click()


        loging_status()
        send_message_normal('Logged in', 'Someone just got logged in', 'NONE-NONE')
        # close_ads()

    except:
        number_of_times_browser_started = number_of_times_browser_started + 1

        if number_of_times_browser_started == 5:
            send_message_normal('Browser Problem', "Browser dosen't started", 'NONE-NONE')

        else:
            start_browser(number_of_times_browser_started)

def start_browser(number_of_times_browser_started):
    global driver

    # driver = webdriver.Firefox()
    driver = webdriver.Chrome("C:/chromedriver.exe", chrome_options = options)
    driver.get(URL)

    login(number_of_times_browser_started)

def text_to_int(price):

    int_price = int(price[0] + price[1] + price[3] + price[4] + price[5])
    return int_price

def last_weeks_highest_average():
    request = requests.get('https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD&guccounter=1')
    content = request.content
    soup = BeautifulSoup(content, 'html.parser')

    highest = 0

    for i in range(72, 163, 15):
        highest = highest + text_to_int(soup.find('span', attrs={'data-reactid': i }).get_text())

    return round((highest) / 7)

def last_weeks_lowest_average():
    request = requests.get('https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD&guccounter=1')
    content = request.content
    soup = BeautifulSoup(content, 'html.parser')

    lowest = 0

    for i in range(74, 165, 15):
        lowest = lowest + text_to_int(soup.find('span', attrs={'data-reactid': i }).get_text())

    return ( round((lowest) / 7))

def last_weeks_hig_low_average():

    highest_average = last_weeks_highest_average()
    lowest_average = last_weeks_lowest_average()

    return (round((highest_average + lowest_average) / 2))

def todays_highest():
    request = requests.get('https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD&guccounter=1')
    content = request.content
    soup = BeautifulSoup(content, 'html.parser')

    return text_to_int(soup.find('span', attrs={'data-reactid':'57'}).get_text())

def todays_lowest():
    request = requests.get('https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD&guccounter=1')
    content = request.content
    soup = BeautifulSoup(content, 'html.parser')

    return text_to_int(soup.find('span', attrs={'data-reactid':'59'}).get_text())

def todays_hig_low_average():
    todays_hig = todays_highest()
    todays_low = todays_lowest()

    return (round((todays_hig + todays_low) / 2))

def money_perday(days, gap, cp_increase_by, invested_money, no_of_times_perday):

    # cp = findingStockPrice()
    cp = 53000

    print ('\n\n\n||========================================||')
    print ('|| Current BTC-USD Price      :', cp)
    print ('|| Invested Money             :', invested_money)
    print ('|| Assumed Gap                :', gap)
    print ('|| Assumed CP Increased By    :', cp_increase_by)
    print ('|| Number Of Cycle Per Day    :', no_of_times_perday)
    print ('|| Number Of Days             :', days)
    print ('||========================================||\n\n\n')

    for i in range(1, days + 1):
        if i < 11 or i % 15 == 0 or i == days:
            invested_money = invested_money + round(((invested_money * (cp + gap - cp)) / cp ) * no_of_times_perday, 2)

            if i == 1:
                print ('\n|-----------------------------------------|\n|')

            else:
                print ('|\n|-----------------------------------------|\n|')

            print ('| Day                   :', i)
            print ('| Assumed BTC-USD Price :', cp)
            print ('| Earned                :', round(invested_money, 2))

            if i == days:
                print('|\n|-----------------------------------------|')

            cp = cp + cp_increase_by

def timmer(time_in_sec):
    for i in range(101):
            sys.stdout.write('\r')
            sys.stdout.write("[%-100s] %d%%" % ('='*i, 1*i))
            sys.stdout.flush()
            time.sleep(time_in_sec)
