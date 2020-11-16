import discord
import dealsListener
import asyncio
from threading import Thread

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await checkDeals()
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$setChannel'):
        print(str(message.channel.id))
        await message.channel.send("Channel set: " + "<#" + str(message.channel.id) + ">")
        channelList.append(message.channel.id)
        sendDeals()

channelList = []
def sendDeals():
    print(channelList)

async def sendMessageToChannel(channelID, message):
    channel = client.get_channel(channelID)
    await channel.send(message)

async def checkDeals():
    d = dealsListener.checkForDeals()
    recentPosts = [d[0]]
    newPosts = [d[1]]
    if len(channelList) > 0:
        for channelID in channelList:
            await sendMessageToChannel(channelID, recentPosts[0]["title"])
    await asyncio.sleep(10)
    await checkDeals()

try:
    #read token
    f = open("token.txt")
    token = f.read()
    f.close()
except:
    print("something wrong with the token...")
else:
    #dealsListener = Thread(target = dealsListener.checkForDeals, args = [3])
    #discord = Thread(target = client.run, args = [token])
    #discord.start()
    #dealsListener.start()
    client.run(token)
