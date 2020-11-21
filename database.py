import os
import psycopg2



def connectToDB():
    DATABASE_URL = os.environ['DISCORD-BOT-DB-LINK']
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    return conn


def loadChannelList():
    try:
        conn = connectToDB()
        cur = conn.cursor()
        cur.execute("SELECT * FROM channelList;")
        channelListTuple = cur.fetchall()
        channelList = dict(channelListTuple)
        print(len(channelList))
        print(sum(channelList.values()))
        #for channel in channelList:
        #    print(channel, channelList[channel])
        cur.close()
        conn.close()
        return channelList
    except Exception as e:
        print(type(e))
        print(e.args)
        print(e)
        print("ERROR LOADING CHANNELS, check DB")
        return {}




def addDealChannel(id, channelList):
    if id not in channelList:
        try:
            channelList[id] = False
            conn = connectToDB()
            cur = conn.cursor()
            cur.execute("INSERT INTO channelList(channelID, ping) VALUES (%s, %s)", (id, False))
            conn.commit()
            cur.close()
            conn.close()
            return " channel added."
        except Exception as e:
            channelList.pop(id, None)
            conn.rollback()
            print(type(e))
            print(e.args)
            print(e)
            cur.close()
            conn.close()
            return " channel could not be added."
    return " channel already registered."

def removeDealChannel(id, channelList):
    try:
        channelList.pop(id, None)
        conn = connectToDB()
        cur = conn.cursor()
        cur.execute("DELETE FROM channelList WHERE channelID = %s;", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return " channel removed."
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)
        return " channel could not be removed."

def managePing(id, channelList, condition):
    if id not in channelList:
        return " you have to add a channel first before enabling/disabling ping feature."
    status = channelList.get(id)
    if status != condition:
        try:
            channelList[id] = condition
            conn = connectToDB()
            cur = conn.cursor()
            cur.execute("UPDATE channelList SET ping = %s WHERE channelList.channelID = %s;", (condition, id))  
            conn.commit()
            cur.close()
            conn.close()
            return " pings set to " + str(condition)
        except Exception as e:
            conn.rollback()
            channelList[id] = status
            print(type(e))
            print(e)
            cur.close()
            conn.close()
            print(" ")
            return " something went wrong... pings reverted to " + str(status)

def loadLastGuid():
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM guidTable;")
    guid = str(cur.fetchone()[0])
    cur.close()
    conn.close()
    return guid

def saveLastGuid(guid):
    try:
        intguid = int(guid)
        conn = connectToDB()
        cur = conn.cursor()
        cur.execute("UPDATE guidTable SET guid = %s;", (intguid,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        conn.rollback()
        conn.close()
        print(type(e))
        print(e)

def testStuff():
    conn = connectToDB()
    cur = conn.cursor()
    #cur.execute("SELECT * FROM channelList;")
    #print(cur.fetchall())
    #cur.execute("DROP TABLE channelList;")
    #cur.execute("CREATE TABLE guidTable(guid int UNIQUE, PRIMARY KEY (guid));")
    try:
        print(cur.rowcount)
        cur.execute("UPDATE guidTable SET guid = %s;", (755405,))        
        print(cur.rowcount)
        #cur.execute("INSERT INTO guidTable(guid) VALUES (%s)", (755409,))
    except Exception as e:
        conn.rollback()
        print(type(e))
        print(e)
        print("channel already exists...")
    cur.execute("SELECT * FROM guidTable;")
    #conn.commit()
    print(cur.fetchall())
    cur.close()
    conn.close()

#testStuff()