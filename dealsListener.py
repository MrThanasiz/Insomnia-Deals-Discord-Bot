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

def getRecentPosts(channel, recentPosts): #gets and returns latest page of posts
    recentPosts = []
    for post in channel:
        if post.tag == "item":
            postData = getPostData(post)
            recentPosts.append(postData)
    return recentPosts

def getNewPosts(channel, recentPosts):   #gets & returns new posts not in list
    newPosts = []
    for post in channel:
        if post.tag == "item":
            postData = getPostData(post)
            if postData["guid"] in recentPosts:
                break
            else:
                newPosts.append(postData)
                recentPosts.append(postData)
    return [recentPosts, newPosts]

async def postsListener():
    print("ok...")


url = "https://www.insomnia.gr/forums/forum/56-%CF%80%CF%81%CE%BF%CF%83%CF%86%CE%BF%CF%81%CE%AD%CF%82.xml/?sortby=start_date&sortdirection=desc"

def parseURL(url):
    opener = urllib.request.build_opener()
    opener.addheaders = []
    tree = ET.parse(opener.open(url))
    root = tree.getroot()
    return root[0]

guid = 0
def checkForDeals():
    channel = parseURL(url)
    print("Latest GUID" + getLatestGuid(channel))
    recentPosts = []
    recentPosts, newPosts = getNewPosts(channel, recentPosts)
    print(recentPosts[0]["title"])
    return recentPosts


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