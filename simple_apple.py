import urllib
from lxml import etree
def getTree():
    r = urllib.urlopen("http://www.appledaily.com.tw/realtimenews/article/finance/20160227/804725/")
    return etree.HTML(r.read().lower().decode('utf-8'))

