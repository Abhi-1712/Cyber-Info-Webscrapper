import os
import telebot
import time
from datetime import date
import ctf
import CyberExperts
import cybernews
import random
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['Help'])
def menu(message):
  help_text="""
The following commands can be executed on the bot: \n
1)"/Greet": Greet the bot \n
2)"/TimeTable": Get the ctf TimeTable from www.ctftime.org \n
3)"/Experts": Get the list of most followed CyberExperts on Twitter \n
4)"/News" : Get the latest Cyber News
"""
  
  bot.send_message(message.chat.id,help_text)

  

@bot.message_handler(commands=['Greet'])
def greet(message):
    greetings=["Hey! How's it going?",'Hey!','Whatsup','Yo!','Glad to meet you!','Hello!']
    bot.reply_to(message,random.choice(greetings))


@bot.message_handler(commands=['TimeTable'])
def TimeTable(message):
  current_date_format=date.today()
  with open('Track/Month.txt') as f:
    for line in f:
      current_month=line
  if int(current_month)!=current_date_format.month:
    ctf.get_timetable()
    with open('Track/Month.txt','w') as f:
        f.write(f'{current_date_format.month}')
  time.sleep(2)
  bot.send_photo(message.chat.id,photo=open('ctf-timetable/timetable.png', 'rb'),caption="For more information visit www.ctftime.org")

@bot.message_handler(commands=['Experts'])
def Experts(message):
  CyberExperts.get_experts()
  Names=[]
  Twitter_IDs=[]
  with open("CyberExperts/ExpertName.txt","r") as NameFile:
    for line in NameFile:
      Names.append(line)
  with open("CyberExperts/TwitterProfile.txt","r") as ID_File:
    for line in ID_File:
      Twitter_IDs.append(line)
  
  result="https://twitter.com/\n\n"
  for index in range(len(Names)):
    result += f"{index+1}: {Names[index]}:{Twitter_IDs[index]}\n"
  
  bot.send_message(message.chat.id,result)
  
  
@bot.message_handler(commands=['News'])
def News(message):
  current_date_format=date.today()
  with open('Track/Day.txt') as f:
    for line in f:
      current_day=line
  if int(current_day)!=current_date_format.day:
    cybernews.get_news()
    with open('Track/Day.txt','w') as f:
      f.write(f'{current_date_format.day}')
  Headlines=[]
  Description=[]
  Links=[]
  with open("cybernews/Headlines.txt") as Headlines_file:
    for line in Headlines_file:
      Headlines.append(line)
  with open("cybernews/Description.txt") as Description_file:
    for line in Description_file:
      Description.append(line)

  with open("cybernews/links.txt") as links_file:
    for line in links_file:
      Links.append(line)
      
      
  for i in range(len(Headlines)):
    try:
      bot.send_photo(message.chat.id,photo=open(f'cybernews_cover_images/{i}.jpg', 'rb'),caption=f"*{Headlines[i]}*\n{Description[i]}\n{Links[i]}",parse_mode="markdown")
    except:
      continue

    


bot.polling()

