import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

try:
    #read token
    f = open("token.txt")
    token = f.read()
    f.close()
except:
    print("something wrong with the token...")
else:
    client.run(token)

