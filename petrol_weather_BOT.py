import logging
import os
PORT = int(os.environ.get('PORT', '8443'))
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



import pandas as pd
import numpy as np
from datetime import date
from datetime import timedelta

  
# Returns the current local date
today = date.today()
yesterday=today-timedelta(days = 1)
print("Today date is: ", today,yesterday)
############### Petrol web scraping ################
import requests
import pandas as pd
from bs4 import BeautifulSoup

def getdata(url):
    r=requests.get(url)
    return r.text
htmldata = getdata("https://www.goodreturns.in/petrol-price.html")
soup = BeautifulSoup(htmldata,'html.parser')
mydata = ''
result = []

for table in soup.find_all('tr'):
    mydata += table.get_text()

mydata = mydata[1:]
iteml = mydata.split("\n\n")
for item in iteml[:-5]:
    result.append(item.split("\n"))
df = pd.DataFrame(result[:-8])
df['City']=(df[0])
df['Today']=(df[1])
df['Yesterday']=(df[2])

y=df[['City','Yesterday','Today']]
Result=y[1:]
Result
x=Result.reset_index(drop=True)
print(x)

############### Weather web scraping ################
from bs4 import BeautifulSoup
import requests
import numpy as np
page = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")

soup = BeautifulSoup(page.content, 'html.parser')

forecast = soup.find(id="seven-day-forecast")
forecast_items = forecast.find_all(class_="tombstone-container")
tonight = forecast_items[1]

#forecast
period = tonight.find(class_="period-name").get_text()
description = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()
#print(period)
#print(description)
#print(temp)

img = tonight.find("img")
desc = img['title']
#print(desc)
period_tags = forecast.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
#periods
short_desc = [sd.get_text() for sd in forecast.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in forecast.select(".tombstone-container .temp")]
temp = [t.get_text() for t in forecast.select(".tombstone-container .temp")]
desc = [d["title"] for d in forecast.select(".tombstone-container img")]
#print(short_desc)
#print(temps)
#print(desc)
import pandas as pd
weather = pd.DataFrame({"Period": periods,"Title": short_desc,"Temperature/F": temps,"Details":desc})
#weather
weather['Temperature'] = weather['Temperature/F'].str.extract('(\d+)').astype(int)

weather['Variance']= weather['Temperature']-(np.mean(weather['Temperature']))
print(weather)
weather


import telebot
token = '1885204428:AAEsNFt184Nf_lLeh5HbQGltl5JDeTD8HJ4'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["help"])
def send_help(message):
    bot.reply_to(message,"Hello welcome, please click on /petrol or /weather to get petrol and weather info.\n Click on /exit to get the exit the session.\n Thank You!")
    
@bot.message_handler(commands=["petrol"])
def echo_all(message):
    bot.reply_to(message,f" Petrol Price as on {today} and {yesterday} \n{x},{message.text} \n Click on /weather to get the weather info.\n Click on /exit to exit the session")
    
@bot.message_handler(commands=["weather"])
def echo_all(message):
    bot.reply_to(message,f" Weather Report California \n{weather},{message.text}\n Click on /petrol to get the petrol price info.\n Click /exit to exit the session")    

@bot.message_handler(commands=["exit"])
def echo_all(message):
    bot.reply_to(message,f"Thank you for using the BOT!\n Have a nice day!")    
    
    
bot.polling()   


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN,
        webhook_url='https://arvindh-anand.herokuapp.com/' + TOKEN
    )

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()