from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as BeautifulSoup
import string
import requests
def getSearchResults(userQuery):
	#seartext = input("enter the search term: ")
	seartext = str(userQuery)
	adlt = 'off' # can be set to 'moderate'
	sear=seartext.strip()
	sear=sear.replace(' ','+')
	URL='https://bing.com/search?q=' + sear
	#print(URL)
	USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
	headers = {"user-agent": USER_AGENT}
	resp = requests.get(URL, headers=headers)
	results=[]
	soup = BeautifulSoup(resp.content, "html.parser")
	#print(soup.li)
	#print(soup)
	wow = soup.find_all('li',class_='b_algo')
	searchResults = []
	count = 0;
	for i in wow:
		try:
			if count >= 5:
				break
			#get links
			searchResults.append(i.h2.a['href'])
			count += 1
		except:
			pass
	return searchResults