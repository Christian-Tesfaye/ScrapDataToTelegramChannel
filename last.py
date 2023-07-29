from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import time
from bs4 import BeautifulSoup

button1 = InlineKeyboardButton(text="Politics", callback_data="function1")
button2 = InlineKeyboardButton(text="Buisness", callback_data="function2")
keyboard_inline = InlineKeyboardMarkup().add(button1,button2)



bot = Bot(token='5810719434:AAFU43cnz9DzBl9s8R-Ino3RHbflIjPzW70')
dp = Dispatcher(bot)

#Set up bot and channel information
bot_token = "5810719434:AAFU43cnz9DzBl9s8R-Ino3RHbflIjPzW70"
channel_id = "-1001826934314"

# Define function to send message to Telegram channel
def send_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": channel_id, "text": message}
    requests.post(url, json=payload)

# Define function to send image to Telegram channel
def send_image(image_path):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    params = {
        'chat_id': channel_id,
        'photo':  image_path,
    }
    requests.get(url, params=params)

# Define function to send text and image to Telegram channel open(image_path, "rb")
def send_data(text_list, image_list, text_list1):
    for i in range(len(text_list)):
        send_message(text_list[i])
        send_image(image_list[i])
        send_message(text_list1[i])
        time.sleep(5)

async def accessCollections(url):
    name13M = []
    img13M = []
    price13M = []
    imdiv1 =[]
    src = requests.get(url)
    soup = BeautifulSoup(src.text,'html.parser')
    #print(soup)
    collections13 = soup.find_all("article")
    # header2 = soup.find('h1', class_="title title--primary").get_text(strip=True)
    #print(len(collections13))
    for col in collections13:
        nm = col.find('h2').get_text(strip=True)
        #date
        imdiv1 = col.find("span",class_="cm-post-date human-diff-time-display").text.strip()
        #description
        imdiv2 = col.find("div", class_="cm-entry-summary").text.strip()
        #img
        img13M=col.find("img")["src"]if col.find("img") else "Image URL not found"
        name13M.append(nm)
        price13M.append(imdiv2)
    send_data(name13M, img13M, price13M)



@dp.message_handler(commands=['News'])
async def postCollections(message:types.Message):
    await message.reply("Select News ", reply_markup=keyboard_inline)


@dp.message_handler(commands=['start'])
async def first(message: types.Message):
    await message.reply("welcome to habeshanews")

@dp.callback_query_handler(text = ["function1", "function2"])
async def accessCollecctions2(call: types.CallbackQuery):
    if call.data == "function1":
        await accessCollections('https://ethiopianmonitor.com/category/politics/')
    elif call.data == "function2":
        await call.message.answer(accessCollections('https://ethiopianmonitor.com/category/buisness/'))
    await call.answer()

executor.start_polling(dp)