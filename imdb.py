import requests as req
from bs4 import BeautifulSoup as bs

def find_by_name(name):
	'''
	This function searches IMDB by the name of actor/actress and scrapes 
	necessary data from IMDB and returns an array of dicts.
	Return at maximum top 50 actor/actresses for the search query.
	'''
	r = req.get('http://www.imdb.com/search/name?name='+name)
	soup = bs(r.text)
	table = soup.find( "table", {"class":"results"})
	rows = table.findAll('tr')
	rows.pop(0)
	query_result = []
	for i,row in enumerate(rows):
		col = {}
		ro = row.find("td", {"class":"name"})
		link = ro.find('a')
		
		name = link.string
		profile_link = link['href']
		image_link = row.find('img')["src"]
		bio = ro.find("span",{"class":"bio"})
		
		col["name"] = name
		col["actor_id"] = profile_link.split('/')[2] 
		col["image_link"] = image_link
		if bio is None:
			col["bio"] = ""
		else:
			col["bio"] = bio.text
		query_result.append(col)
	return query_result
		
#find_by_name('shah')
