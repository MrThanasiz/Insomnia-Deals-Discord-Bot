import xml.etree.ElementTree as ET
import urllib.request
import html2markdown
import database
import re

urlPage = "https://www.insomnia.gr/forums/forum/56-%CF%80%CF%81%CE%BF%CF%83%CF%86%CE%BF%CF%81%CE%AD%CF%82.xml/?sortby=start_date&sortdirection=desc"
pageNo = 2 ## urlPageN Doesn't work
#urlPageN = "https://www.insomnia.gr/forums/forum/56-%CF%80%CF%81%CE%BF%CF%83%CF%86%CE%BF%CF%81%CE%AD%CF%82/page/" +  str(pageNo) + ".xml/?sortby=start_date&sortdirection=desc"

def parseURL(url):
    opener = urllib.request.build_opener()
    opener.addheaders = []
    tree = ET.parse(opener.open(url))
    root = tree.getroot()
    return root[0]

def getLatestGuid(channel):
    for post in channel:
        if post.tag == "item":
            for info in post:
                if info.tag == "guid":
                    return(info.text)



def getNewPosts(channel, guid): #Returns posts after given Guid
    newPosts = []
    for post in channel:
        if post.tag == "item":
            postData = getPostData(post)
            if int(postData["guid"]) <= int(guid):
                break
            else:
                newPosts.append(postData)
    return newPosts

def getRecentPosts(channel): #Returns page of posts
    recentPosts = []
    for post in channel:
        if post.tag == "item":
            postData = getPostData(post)
            recentPosts.append(postData)
    return recentPosts

def getPostData(post):
    postData = {}
    postData["title"] = post[0].text
    postData["link"] = post[1].text
    postData["desc"] = post[2].text
    postData["guid"] = post[3].text
    postData["date"] = post[4].text
    return postData

def debugPrintPost(posts):
    if len(posts)>0:
        print("debug printing posts:")
        for post in posts:
            printPost(post)
        print("debug end")
    else:
        print("debug: No posts")

def printPost(post):
    print("Title: " + post["title"] + " guid: " + 
    post["guid"] + " date: " + post["date"] + " link: " + post["link"])
    print("desc: " + post["desc"])


def checkForDeals(): #(Main)
    print("Checking for deals... (dealsListener.py)")
    
    try:
        channel = parseURL(urlPage)
    except Exception as e:
        print(type(e))
        print(e)
        return []

    latestGuid = getLatestGuid(channel)
    try:
        lastGuid = database.loadLastGuid()
    except:
        lastGuid = latestGuid
        database.saveLastGuid(lastGuid)
    
    print("LatestGuid: " + latestGuid + " LastGuid: " + lastGuid)
    #lastGuid = "755196" #TODO DEBUG REMOVE
    if latestGuid > lastGuid:
        newPosts = getNewPosts(channel, lastGuid)
        #newPosts = getRecentPosts(channel) #TODO DEBUG REMOVE
        lastGuid = latestGuid
        database.saveLastGuid(lastGuid)
        #debugPrintPost(newPosts)
        return newPosts
    else:
        return []

def cleanPostDescription(desc):
    desc = desc.replace('rel="external"','')
    desc = html2markdown.convert(desc)
    desc = desc.replace("\n\n", "\n")
    #html codes to char
    #TODO automate ambers to its translation
    desc = desc.replace("&nbsp;", " ")
    desc = desc.replace("&lt;", "<")
    desc = desc.replace("&gt;", ">")
    #removal of problematic tags
    desc = desc.replace("<u>", "")
    desc = desc.replace("</u>", "")
    desc = re.sub("<img alt=([\w\W]+?)/>", "~~IMAGE~~", desc)
    desc = desc.replace("<span>", "")
    desc = desc.replace("</span>", "")
    desc = desc.replace("</h1>", "")
    desc = re.sub("<span([\w\W]+?)>", "~~SPAN~~", desc)
    desc = re.sub("<h1([\w\W]+?)>", "~~H1~~", desc)
    desc = re.sub("<a([\w\W]+?)>", "~~ASTART~~", desc)
    desc = desc.replace("</a>", "~~AEND~~")
    print(repr(desc))
    return desc[:2047]


#TODO Iframe remove!
#<iframe allowfullscreen="" data-embed-src="https://www.insomnia.gr/forums/topic/742059-ps-plus-34-%CE%B5%CF%85%CF%81%CF%8E-%CE%AD%CF%84%CE%BF%CF%82-8-%CE%B5%CF%85%CF%81%CF%8E-%CE%BC%CE%AD%CE%BD%CE%BF%CF%85%CE%BD-%CF%83%CF%84%CE%BF-wallet/?do=embed" data-embedauthorid="432048" data-embedcontent="" data-embedid="embed2515163614" 
#scrolling="no" style="height:387px;max-width:502px;"></iframe>

#Strong, BR fix TODO
#Γίνετε μέλος στο Miles+Bonus μέχρι την 01.12.2020 και κερδίστε <strong style="background-color:#e6e5ea;border:0px;color:#444444;font-size:16px;padding:0px;text-align:left;vertical-align:baseline;">5.000 μίλια εξαργύρωσης,</strong>SPAN τα οποία μπορείτε να εξαργυρώσετε σε ένα ταξίδι εσωτερικού όποτε και σε όποιο προορισμό επιθυμείτε! Κάντε σήμερα την εγγραφή σας και επωφεληθείτε από την προσφορά!
#<br style="background-color:#e6e5ea;color:#444444;font-size:16px;text-align:left;"/>

#
#<div class="ipsEmbeddedVideo">
#<div>
#<iframe allowfullscreen="" data-embed-src="https://www.youtube.com/embed/lGNC_FTLXOg?feature=oembed" frameborder="0" height="270" width="480"></iframe>
#</div>
#</div>