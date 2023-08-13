from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import time

from bs4 import BeautifulSoup


button1 = InlineKeyboardButton(text="Latest", callback_data="function1")
button2 = InlineKeyboardButton(text="Buisness", callback_data="function2")
button3 = InlineKeyboardButton(text="Health", callback_data="function3")
button4 = InlineKeyboardButton(text="crime", callback_data="function4")
button5 = InlineKeyboardButton(text="Science and Tech", callback_data="function5")
button6 = InlineKeyboardButton(text="Politics", callback_data="function6")
keyboard_inline = InlineKeyboardMarkup().add(button1,button2,button3,button4,button5,button6)



bot = Bot(token='')
dp = Dispatcher(bot)

#Set up bot and channel information
bot_token = " "
channel_id = " "

# Define function to send message to Telegram channel
def send_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": channel_id, "text": message}
    requests.post(url, json=payload)


# Define function to send text and image to Telegram channel open(image_path, "rb")

def send_data(text_list):
    for i in range(len(text_list)):
        send_message(text_list[i])
        
        time.sleep(2)
async def accessCollections(url):
    cont = []
    src = requests.get(url)
    soup = BeautifulSoup(src.text,'html.parser')
    
    collections13 = soup.find_all("article")
 
    for col in collections13:
        img=col.find("img")["src"]if col.find("img") else "Image URL not found"
        title = col.find('h2').text.strip()
        date = col.find("span",class_="cm-post-date human-diff-time-display").text.strip()
        description= col.find("div", class_="cm-entry-summary").text.strip()
        link=col.find("a",class_="cm-entry-button")["href"]
        
      
        all=f"{img}\n\n{title}\n\n{date}\n\n{description}\n{link}"
        cont.append(all)
    send_data(cont)




@dp.message_handler(commands=['News'])
async def postCollections(message:types.Message):
    await message.reply("Select News ", reply_markup=keyboard_inline)


@dp.message_handler(commands=['start'])
async def first(message: types.Message):
    await message.reply("welcome to Habesha News")
    await message.reply("type'/News' to get news")

@dp.callback_query_handler(text = ["function1", "function2","function3","function4","function5","function6"])
async def accessCollecctions2(call: types.CallbackQuery):
    if call.data == "function1":
        await accessCollections('https://ethiopianmonitor.com/category/news/')
    elif call.data == "function2":
        await accessCollections('https://ethiopianmonitor.com/category/business/')
    elif call.data == "function3":
        await accessCollections('https://ethiopianmonitor.com/category/health/')
    elif call.data == "function4":
        await accessCollections('https://ethiopianmonitor.com/category/crime/')
    elif call.data == "function5":
        await accessCollections('https://ethiopianmonitor.com/category/science-tech/')
    elif call.data == "function6":
        await accessCollections('https://ethiopianmonitor.com/category/politics/')
    await call.answer()

executor.start_polling(dp)
