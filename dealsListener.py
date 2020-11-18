import xml.etree.ElementTree as ET
import urllib.request
import asyncio
import time

def getLatestGuid(channel):
    for post in channel:
        if post.tag == "item":
            for info in post:
                if info.tag == "guid":
                    return(info.text)

def getPostData(post):
    postData = {}
    postData["title"] = post[0].text
    postData["link"] = post[1].text
    postData["desc"] = post[2].text
    postData["guid"] = post[3].text
    postData["date"] = post[4].text
    return postData

def getRecentPosts(channel, recentPosts): #Returns latest page of posts
    recentPosts = []
    for post in channel:
        if post.tag == "item":
            postData = getPostData(post)
            recentPosts.append(postData)
    return recentPosts

def getNewPosts(channel, guid): #TODO  #Returns posts after given Guid
    newPosts = []
    for post in channel:
        if post.tag == "item":
            postData = getPostData(post)
            if postData["guid"] < guid:
                break
            else:
                newPosts.append(postData)
    return newPosts



url = "https://www.insomnia.gr/forums/forum/56-%CF%80%CF%81%CE%BF%CF%83%CF%86%CE%BF%CF%81%CE%AD%CF%82.xml/?sortby=start_date&sortdirection=desc"

def parseURL(url):
    opener = urllib.request.build_opener()
    opener.addheaders = []
    tree = ET.parse(opener.open(url))
    root = tree.getroot()
    return root[0]

def saveLastGuid(guid):
    f = open("lastGuid", "w+")
    f.write(guid)
    f.close()

def loadLastGuid():
    f = open("lastGuid", "r")
    guid = f.read()
    f.close()
    return guid

def debugPrintPostTitleGuid(posts):
    if len(posts>0):
        print("debug printing posts:")
        for post in posts:
            print("Title: " + post["title"] + " guid: " + post["guid"])
        print("debug end")
    else:
        print("debug: No posts")

def checkForDeals(): #(Main)
    print("Checking for deals...")
    channel = parseURL(url)
    latestGuid = getLatestGuid(channel)
    try:
        lastGuid = loadLastGuid()
    except:
        lastGuid = latestGuid
    print("LatestGuid: " + latestGuid + " LastGuid: " + lastGuid)
    if latestGuid > lastGuid:
        newPosts = getNewPosts(channel, lastGuid)
        lastGuid = latestGuid
        saveLastGuid(lastGuid)
        debugPrintPostTitleGuid(newPosts)
        return newPosts
    else:
        return []


#recentPosts = []
#channel = parseURL(url)
#recentPosts = []
#recentPosts, newPosts = getNewPosts(channel, recentPosts)
#print("Latest post: " + str(recentPosts[0]))
#print("Latest GUID" + getLatestGuid(channel))
##############################

async def main():
    await checkForDeals(5)

#asyncio.run(main())