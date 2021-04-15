# import discord to use the bot
import discord
# to use enviroment variables
import os
# generate random number
import random

#import sellenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# try catch Exception
from selenium.common.exceptions import NoSuchElementException       

# chrome driver options 
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# creating drivers for each website to scrape
microsoft_driver = webdriver.Chrome(options=chrome_options)
google_driver = webdriver.Chrome(options=chrome_options)
amazon_driver = webdriver.Chrome(options=chrome_options)
tech_crunch_driver = webdriver.Chrome(options=chrome_options)

# get html content of the webpage
microsoft_driver.get("https://events.microsoft.com/?timeperiod=next30Days&isSharedInLocalViewMode=false&eventsfor=Students&language=English")

# get the HTML content of webpage
google_driver.get("https://developers.google.com/events")

 # get the HTML content of the page
amazon_driver.get("https://aws.amazon.com/events/explore-aws-events/?events-master-main.sort-by=item.additionalFields.startDateTime&events-master-main.sort-order=asc&awsf.events-master-location=*all&awsf.events-master-type=type%23virtual&awsf.events-master-series=*all&awsf.events-master-audience=*all&awsf.events-master-category=*all&awsf.events-master-level=level%23100")

# get HTML content of the webpage
tech_crunch_driver.get("https://techcrunch.com/")

# get the user
client = discord.Client()

# On ready event
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

# on message event
@client.event
async def on_message(message):
  # if the user is our bot we want to do nothing
  if message.author == client.user:
    return

  # store message content in a variable
  msg = message.content

  # hello event
  if msg.startswith('!hello'):
    await message.channel.send('Hello! How are you ?')
  
  
  elif msg.startswith("!list-commands"):
    await message.channel.send('>>> 1. `!get-microsoft-eve-stud` - Get latest events of Mircosoft for students \n 2. `!get-google-up-eve` - Get latest upcoming events of Google for students \n 3.` !amazon-eve` Get latest upcoming events of Amazon (AWS) for students \n 4.`!get-news` Get latest technology related news ')



# ----------------  Microsoft fetching -------------------


  # get microsoft latest student 
  elif msg.startswith("!get-microsoft-eve-stud"):

    # get the event div using its class name
    event_div = microsoft_driver.find_elements(By.CLASS_NAME, 'eventSection')

    # creating empty arrays to store the 
    # 1. event titles
    list_m_events = []
    # 2. links to those events
    links_reg = []

    # get titles and links to those events
    for event in event_div:
      # get element: titles
      mircosoft_events = event.find_elements(By.CLASS_NAME, 'eventTitle')
      # get element: links
      event_links = event.find_elements(By.CLASS_NAME, 'registerBtnSmall')

      # loop through the event titles and store the text 
      # into list_m_events array
      for e in mircosoft_events:
        # the title must not be empty
        if(e.text != ''):
          list_m_events.append(e.text)

      # loop through the event titles and store the text 
      # into list_m_events array
      for link in event_links:
        links_reg.append(link.get_attribute('href'))
    
    # generate a random index
    random_num = random.randint(0, len(list_m_events) + 1)
    print(len(list_m_events))
    print(random_num)

    if(random_num < len(list_m_events)):
      # send message from the bot
      await message.channel.send(">>> "  + '\n' + list_m_events[random_num] + '\n\n' + 'Registration Link: \n' + links_reg[random_num])

    else:
      await message.channel.send("Couldn't fetch it. Try Again !")


# ---------------------------------------------------------
# --------------- Google events fetching ------------------


# respond to google events command
  elif msg.startswith("!get-google-up-eve"):

    # get the event div
    event_div_g = google_driver.find_elements(By.CLASS_NAME, 'devsite-landing-row-item')

    # creating empty arrays to store
    # 1. Events' banner image
    event_g_image = []  
    # 2. Registration link
    reg_link = []
    # 3. Events' titles
    event_g_title = []

    # looping the through the event_div_g array to get other reuired elements
    for e in event_div_g:
      # using NoSuchElementException
      try:
        # this is done to check whether the div has a register button or not 
        # if it has that means that the event is upcoming and not conducted
        e.find_element(By.CLASS_NAME, 'button-primary')
        linkreg_g = e.find_elements(By.CLASS_NAME, 'button-primary')

        # if it has a button then get the title, link and image
        event_image = e.find_elements(By.TAG_NAME, 'img')
        event_go_title = e.find_elements(By.TAG_NAME, 'h3')

        # store image link into event_g_image array
        for i_link in event_image:
          event_g_image.append(i_link.get_attribute('src'))
        
        # store registration links into reg_link array
        for r_link in linkreg_g:
          reg_link.append(r_link.get_attribute('href'))
        
        # store titles in event_g_title array
        for e_title in event_go_title:
          event_g_title.append(e_title.text)

      except NoSuchElementException:
        print('done')    

    # generate a random index
    random_num_g = random.randint(0, len(reg_link) + 1)

    # send message
    if(random_num_g < len(reg_link)):
      await message.channel.send(">>> " + "\n" + event_g_title[random_num_g] + "\n\n" + "Registration Link :\n" + reg_link[random_num_g] + "\n")
      
      await message.channel.send(event_g_image[random_num_g])

    else:
      await message.channel.send("Couldn't fetch it. Try Again !")


# ---------------------------------------------------------
# ---------------- Amazon events fetching ----------------- 


# respond to amazon events' command
  elif msg.startswith("!amazon-eve"):
    
    event_ama = amazon_driver.find_elements(By.CLASS_NAME, 'm-headline')

    # created empty arrays to store:
    # 1. Titles
    event_ama_title = []
    # 2. Links
    event_ama_link = []

    # looping the through the event_ama array to get other reuired elements
    for event in event_ama:
      event_links = event.find_elements(By.TAG_NAME, 'a')
      
      # get links and event titles
      for link in event_links:
        event_ama_link.append(link.get_attribute('href'))
        event_ama_title.append(link.text)

    # genrate a random index
    random_ama_eve = random.randint(0, len(event_ama_link) + 1)
    print(len(event_ama_link))
    print(random_ama_eve)

    # send message
    if(random_ama_eve < len(event_ama_link)):
      await message.channel.send(">>> " + event_ama_title[random_ama_eve] + "\n\n" + "Registration Link: \n" + event_ama_link[random_ama_eve])
    else:
      await message.channel.send("Couldn't fetch it. Try Again !")

# ----------------------------------------------------------
# ------------------ News fetching -------------------------


# repond to get news message
  elif msg.startswith("!get-news"):

    # get the news div element
    event_news = tech_crunch_driver.find_elements(By.CLASS_NAME, 'post-block__title__link')

    # Created empty array to store:
    # 1. News title
    info_text = []
    # 2. News Link
    info_link = []

    
    # loop through event_news array to get the other reuired elements
    for info in event_news:
      info_text.append(info.text)
      info_link.append(info.get_attribute('href'))

    # generate a random index number
    random_info = random.randint(0, len(info_text) + 1)

    if(random_info < len(info_text)):
      # send message
      await message.channel.send(">>> " + info_text[random_info] + "\n\n To read more: \n" + info_link[random_info])

    else:
      await message.channel.send("Couldn't fetch it. Try Again !")


# dicord bot's token to run it successfully
client.run(os.getenv('TOKEN'))

# quiting the fetching chrome drivers
microsoft_driver.quit()
google_driver.quit()
amazon_driver.quit()
tech_crunch_driver.quit()