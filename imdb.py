import requests as req
from bs4 import BeautifulSoup as bs
import re

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

def get_movie_detail_by_movie_id(movie_id):
	r = req.get('http://www.imdb.com/title/'+movie_id)
	soup = bs(r.text)
	display = soup.find('div',{'class':'poster'})
	display_pic = display.find('a').find('img')['src']
	infobar = soup.find('div',{'class':'subtext'})
	title = soup.find('title').string
	title = title.split('-')[0].strip()
	length = infobar.find('time').string.strip()
	genre_list = infobar.findAll('a')
	for i in range(len(genre_list)-1):
		genre_list[i] = genre_list[i].string
	genre = ','.join(genre_list[i] for i in range(len(genre_list)-1))
	release_date = genre_list[-1].text.strip()
	rate = soup.find('span',itemprop='ratingValue').string
	count = soup.find('span',itemprop='ratingCount').string
	rating = rate + '/10 from ' + count + ' users'
	return display_pic, title, length, genre, release_date

def get_reviews_by_movie_id(movie_id, count=3):
	'''
	Returns top 3 reviews of the movie
	'''
	extra_string = '*** This review may contain spoilers ***'
	r = req.get('http://www.imdb.com/title/'+movie_id+'/reviews')
	soup = bs(r.text)
	text_list = soup.findAll('p',{'class':''})[5:]
	rev = []
	for i in range(count):
		if text_list[i].string == extra_string:
			i-=1
		rev.append(text_list[i])
	text_list = rev
	headings =[heading.string for heading in soup.findAll('h2')[:3]]
	authors = soup.findAll('a', {'href':re.compile('user')})[1:6:2]
	authors = [author.string for author in authors]
	reviews = []
	for i in range(count):
		review = {}
		review['text'] = text_list[i]
		review['heading'] = headings[i]
		review['author'] = authors[i]
		reviews.append(review)
	print reviews[0]
	return reviews

def find_movies_by_actor_id(actor_id):
	'''
	Return top 3 movies by an actor 
	using actor_id
	'''
	r = req.get('http://www.imdb.com/name/'+actor_id)
	soup = bs(r.text)
	movie_div = soup.find("div", {"id":"knownfor"})
	divs = movie_div.findAll("div")
	divs = divs[:3]#To get only Top 3 movies.
	movie_list = []
	for div in divs:
		movie = {}
		url = div.find("a")["href"]
		url = url.split('/')
		movie["movie_id"] = url[2]
		movie["display_pic"],movie["title"],movie["length"],movie["genre"],movie["release_date"] = get_movie_detail_by_movie_id(movie["movie_id"])
		movie_list.append(movie)
	print movie_list
		
#find_by_name('shah')
#find_movies_by_actor_id('nm1229940')
get_reviews_by_movie_id('tt2224317')
