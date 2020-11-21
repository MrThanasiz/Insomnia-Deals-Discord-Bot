import discord
#from discord.ext import commands
import database
import dataManager
import botCommands
import asyncio
import random
import os
from threading import Thread

client = discord.Client()
#bot = commands.Bot(command_prefix= "$") #TODO REFACTOR TO THIS <<<
#TODO make sure user is admin
#TODO help, author, invite
client.channelList = {} # channelID : ping(True False)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    client.channelList = await botCommands.onReadyLoadChannels()
    print(client.channelList)
    stats = "Sending to " + str(len(client.channelList)) + " channels and pinging " + str(sum(client.channelList.values())) + " channels."
    print(stats)
    await sendMessage(DEBUG_CHANNEL, "ΞΕΚΙΝΗΣΑ ΝΑ ΤΡΕΧΩ ΑΦΕΝΤΙΚΟ!")
    await sendMessage(DEBUG_CHANNEL, stats)
    await main()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$dealsAddChannel"):
        channelID = message.channel.id
        res = database.addDealChannel(channelID, client.channelList)
        await message.channel.send("<#" + str(channelID) + ">" + res)
    
    if message.content.startswith("$dealsRemoveChannel"):
        channelID = message.channel.id
        res = database.removeDealChannel(channelID, client.channelList)
        await message.channel.send("<#" + str(channelID) + ">" + res)

    if message.content.startswith("$dealsAddPingChannel"):
        channelID = message.channel.id
        res = database.managePing(channelID, client.channelList, True)
        await message.channel.send("<#" + str(channelID) + ">" + res)
    
    if message.content.startswith("$dealsRemovePingChannel"):
        channelID = message.channel.id
        res = database.managePing(channelID, client.channelList, False)
        await message.channel.send("<#" + str(channelID) + ">" + res)

    if message.content.startswith("$dealsHelp") or message.content.startswith("$dealsCommands"):
        channelID = message.channel.id
        res = botCommands.helpCommand()
        await message.channel.send(res)

    if message.content.startswith("$dealsAuthor") or message.content.startswith("$dealsAbout"):
        channelID = message.channel.id
        res = botCommands.aboutAuthor()
        await message.channel.send(res)


async def sendMessage(channelID, message):
    channel = client.get_channel(channelID)
    await channel.send(message)

async def sendPost(channelID, post):
    print("sending post to channel beep boop :)")
    desc = dataManager.cleanPostDescription(post["desc"])
    embed=discord.Embed(title=post["title"], url=post["link"], description=desc)
    channel = client.get_channel(channelID)
    await channel.send(embed=embed)

async def justSpam(channelList): #TEST FUNCTION
    if len(channelList) > 0:
        for channelID in channelList:
            await sendMessage(channelID, "Hey there :)")
    await asyncio.sleep(random.random()*10)
    await justSpam()

async def dealsChecker(interval): #Interval (in seconds) to check for deals
    print("Checking for deals... (bot.py)")
    print(client.channelList)
    newPosts = dataManager.checkForDeals()
    print(str(len(newPosts)) + " New Posts, sending to " 
    + str(len(client.channelList)) + " channels and pinging " 
    + str(sum(client.channelList.values())) + " channels.")
    if len(client.channelList) > 0 and len(newPosts) > 0:
        for channelID in client.channelList:
            if client.channelList[channelID]:
                await sendMessage(channelID, "@here ΕΡΧΟΝΤΑΙ ΠΡΟΣΦΟΡΕΣΣΣ!!1!")
            for post in newPosts:
                await sendPost(channelID, post)
    await asyncio.sleep(interval)
    await dealsChecker(interval)


async def main():
    # Schedule calls *concurrently*:
    await asyncio.gather(
        dealsChecker(600),
        #justSpam(),
    )


TOKEN = os.getenv("DISCORD_TOKEN_DEALSBOT")
DEBUG_CHANNEL = 777618394236452894
client.run(TOKEN)
#bot.run(TOKEN)
