import database



def aboutAuthor():
    return "Bot author: Thanos#7274 Contact: "

def helpCommand():
    helpText = "gg "
    return helpText

async def onReadyLoadChannels():
    channelList = database.loadChannelList()
    return channelList

#testList = [777618394236452894,777618391136452894,777618394232352894,777618394232341894] 
#testList = []

#saveChannelList("msg", testList)
#outlist = loadChannelList("normal")
#removeDealChannel(777618394232352894, "normal", outlist)
#print(outlist)