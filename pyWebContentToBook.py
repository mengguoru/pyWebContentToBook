import urllib.request
from bs4 import  BeautifulSoup
import  requests
import  json,configparser

#below settings read from config.json
config = configparser.ConfigParser()
with open('config.json', 'r') as f:
    config = json.load(f)
target_url = config["target_url"]
bookName = config["bookName"]

page = urllib.request.urlopen(target_url).read()
soup = BeautifulSoup(page,"html.parser")
# print(soup)
urls = []
writelines = []

for link in soup.find_all('a'):
    s = str(link.text)
    s = s.replace('\n','').replace(' ','')
    url = target_url.replace('/index.htm','') + '/'+ link.get('href')
    if '第' in s:
        writelines.append(s+'\n')
        urls.append(url)

i=0
while len(urls) >i:
    # page2 = urllib.request.urlopen(urls[0]).read()
    # # page2 = page2.decode('gb2312')
    # # print(type(page2))


    t = requests.get(urls[i])
    # print(t.content.decode('gbk'))
    page2 = t.content.decode('gbk')
    soup2 = BeautifulSoup(page2,"html.parser")
    theContents = soup2.find_all('font',attrs={"size":"3"},limit=1)
    for c in theContents:
        text = str(c.text)

        # print(text)
        writelines.append(text)
    i+=1

with open(bookName,'w') as f:
    f.writelines(writelines)