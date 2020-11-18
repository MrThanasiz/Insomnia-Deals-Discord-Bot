import discord
import dealsListener
import asyncio
import random
from threading import Thread

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #await checkDeals()
    #await justSpam()
    #await sendMessage(777618394236452894, "<@778608600867668018> στειλε μου τον αριθμο της καρτα σου και θα ειναι σπιτι σου σε 3 εργασιμες")
    #await sendMessage(777618394236452894, "<@Thanos#7274> τεστ")
    
    await main()
    
    
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$setChannel'):
        print(str(message.channel.id))
        await message.channel.send("Channel set: " + "<#" + str(message.channel.id) + ">")
        await message.channel.send("Channel set: " + "<#" + str(message.channel.id) + ">")
        channelList.append(message.channel.id)
        sendDeals()

channelList = []
def sendDeals():
    print(channelList)

async def sendMessage(channelID, message):
    channel = client.get_channel(channelID)
    await channel.send(message)

async def sendPost(channelID, post):
    print("sending post to channel beep boop :)")

async def justSpam():
    #print("pipis")
    if len(channelList) > 0:
        for channelID in channelList:
            await sendMessage(channelID, "PIPIS PIPA")
    await asyncio.sleep(random.random()*10)
    await justSpam()

async def checkDeals():
    print("checked deals")
    newPosts = dealsListener.checkForDeals()
    if len(channelList) > 0:
        for channelID in channelList:
            for post in newPosts:
                await sendPost(channelID, post)
    await asyncio.sleep(10)
    await checkDeals()

async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        checkDeals(),
        #justSpam(),
    )


try:
    #read token
    f = open("token.txt")
    token = f.read()
    f.close()
except:
    print("something wrong with the token...")
else:
    client.run(token)
