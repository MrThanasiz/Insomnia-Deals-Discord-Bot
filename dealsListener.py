import xml.etree.ElementTree as ET
tree = ET.parse("demo.xml")

root = tree.getroot()
channel = root[0]

for post in channel:
    if post.tag == "item":
        for info in post:
            print(info.tag)
            print(info.text)
            #print((info.text).encode("utf-8"))