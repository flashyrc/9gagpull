import requests
from bs4 import BeautifulSoup
import os
import json
from sys import argv
from urlparse import urlparse
from os.path import splitext, basename

#Add proxies if required (normally we have to if we are at workplace ;))
proxies = {
  "http": "http://<uname>:<pwd>@xxx.xxx.xxx:xxxx",
  "https": "http://<uname>:<pwd>@xxx.xxx.xxx:xxxx",
}

def openImages(gagurls):
	imageurls = ''
	for u in gagurls:
		r = requests.get(u, proxies=proxies)
		soup = BeautifulSoup(r.text)
		
		for img in soup.find_all('img', class_='badge-item-img'):
			#imageurls = imageurls + '"' + img['src'] + '" '
			imgurl = img['src']
			disassembled = urlparse(imgurl)
			filename, file_ext = splitext(basename(disassembled.path))
			f = open('<FOLDER_TO_STORE_IMAGES>' + filename + file_ext, 'wb')
			f.write(requests.get(img['src'], proxies=proxies).content)
			f.close()
		
def getImages(pagenum):
	gagurls = []
	if pagenum == 0:
		gagurls.append('http://9gag.com')
	else:
		r2 = requests.get('http://d24w6bsrhbeh9d.cloudfront.net/read/ajax-featured?pageType=hot&page=' + str(pagenum) + '&callback=data', proxies=proxies)
		x = json.loads(r2.text[5:][0:-2])
		for y in x['result']:
			gagurls.append(y['url'])
	openImages(gagurls)
	
def main():
	script, pagenumstr = argv
	pagenum = int(pagenumstr)
	getImages(pagenum)
	
if __name__ == '__main__':
	main()
