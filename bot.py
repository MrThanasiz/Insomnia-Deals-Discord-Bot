import discord
#from discord.ext import commands
import dataManager
import botCommands
import asyncio
import random
import os
from threading import Thread

client = discord.Client()
#bot = commands.Bot(command_prefix= "$") #TODO REFACTOR TO THIS <<<

client.msgChannelList = []
client.pingChannelList = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(client.msgChannelList)
    print(client.pingChannelList)
    client.msgChannelList, client.pingChannelList = await botCommands.onReadyLoadChannels(MESSAGE_CHANNEL_FN, PING_CHANNEL_FN)
    print("Sending to " + str(len(client.msgChannelList)) + " channels and pinging " + str(len(client.pingChannelList)) + " channels.")
    await sendMessage(777618394236452894, "ΞΕΚΙΝΗΣΑ ΝΑ ΤΡΕΧΩ ΑΦΕΝΤΙΚΟ!")
    await main()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$dealsAddChannel"):
        channelID = message.channel.id
        res = botCommands.addDealChannel(channelID, MESSAGE_CHANNEL_FN, client.msgChannelList)
        await message.channel.send("<#" + str(channelID) + ">" + res)
    
    if message.content.startswith("$dealsRemoveChannel"):
        channelID = message.channel.id
        res = botCommands.removeDealChannel(channelID, MESSAGE_CHANNEL_FN, client.msgChannelList)
        await message.channel.send("<#" + str(channelID) + ">" + res)

    if message.content.startswith("$dealsAddPingChannel"):
        channelID = message.channel.id
        res = botCommands.addDealChannel(channelID, PING_CHANNEL_FN, client.pingChannelList)
        await message.channel.send("<#" + str(channelID) + ">" + res)
    
    if message.content.startswith("$dealsRemovePingChannel"):
        channelID = message.channel.id
        res = botCommands.removeDealChannel(channelID, PING_CHANNEL_FN, client.pingChannelList)
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
    print(client.msgChannelList)
    newPosts = dataManager.checkForDeals()
    print(str(len(newPosts)) + " New Posts, sending to " 
    + str(len(client.msgChannelList)) + " channels and pinging " 
    + str(len(client.pingChannelList)) + " channels.")
    if len(client.msgChannelList) > 0 and len(newPosts) > 0:
        for channelID in client.msgChannelList:
            if channelID in client.pingChannelList:
                await sendMessage(channelID, "@here ΕΡΧΟΝΤΑΙ ΠΡΟΣΦΟΡΕΣΣΣ!!1!")
            for post in newPosts:
                await sendPost(channelID, post)
    await asyncio.sleep(interval)
    await dealsChecker(interval)


async def main():
    # Schedule calls *concurrently*:
    await asyncio.gather(
        dealsChecker(100),
        #justSpam(),
    )


MESSAGE_CHANNEL_FN = "msgChannelList"
PING_CHANNEL_FN = "pingChannelList"
TOKEN = os.getenv("DISCORD_TOKEN_DEALSBOT")
client.run(TOKEN)
#bot.run(TOKEN)
