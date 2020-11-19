def loadChannelList(listType): #Private
    try:
        f = open(listType, "r")
        channelList = []
        count = 0
        while True: 
            line = f.readline()
            if not line: 
                print(listType + " contains " + str(count) + " channels")
                return channelList
            count += 1
            channelList.append(int(line))
    except Exception as e:
        print(type(e))
        print(e.args)
        print(e)
        print(listType + " file does not exist")
        return []


def saveChannelList(listType, channelList): #Private
    f = open(listType, "w+")
    for channel in channelList:
        f.write(str(channel) + "\n")
    f.close()

def addDealChannel(id, listType, channelList):
    if id not in channelList:
        try:
            channelList.append(id)
            saveChannelList(listType,channelList)
            return " channel added."
        except Exception as e:
            print(type(e))
            print(e.args)
            print(e)
            return " channel could not be added."
    return " channel already registered."

def removeDealChannel(id, listType, channelList):
    try:
        channelList.remove(id)
        saveChannelList(listType,channelList)
        return " channel removed."
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)
        return " channel was not in list or could not be removed."

def aboutAuthor():
    return "Bot author: Thanos#7274 Contact: "

def helpCommand():
    helpText = "gg "
    return helpText

async def onReadyLoadChannels(msgChannelFN, pingChannelFN):
    msgChannelList = loadChannelList(msgChannelFN)
    pingChannelList = loadChannelList(pingChannelFN)
    return msgChannelList, pingChannelList

#testList = [777618394236452894,777618391136452894,777618394232352894,777618394232341894] 
#testList = []

#saveChannelList("msg", testList)
#outlist = loadChannelList("normal")
#removeDealChannel(777618394232352894, "normal", outlist)
#print(outlist)