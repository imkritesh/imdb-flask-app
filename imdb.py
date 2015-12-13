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
	title = title.split('-')
	title = '-'.join(title[i] for i in range(len(title)-1)).strip()
	length = infobar.find('time').string.strip()
	genre_list = infobar.findAll('a')
	for i in range(len(genre_list)-1):
		genre_list[i] = genre_list[i].string
	genre = ','.join(genre_list[i] for i in range(len(genre_list)-1))
	release_date = genre_list[-1].text.strip()
	rate = soup.find('span',itemprop='ratingValue')
	count = soup.find('span',itemprop='ratingCount')
	if rate and count:
		rate = rate.string
		count = count.string
		rating = rate + '/10 from ' + count + ' users'
	else:
		rating = 'Not Yet Released'
	return display_pic, title, length, genre, release_date, rating

def get_reviews_by_movie_id(movie_id, count=3):
	'''
	Returns top 3 reviews of the movie
	'''
	extra_string = '*** This review may contain spoilers ***'
	extra_string2 = 'Find showtimes, watch trailers, browse photos, track your Watchlist and rate your favorite movies and TV shows on your phone or tablet!'
	r = req.get('http://www.imdb.com/title/'+movie_id+'/reviews')
	soup = bs(r.text)
	text_list = soup.findAll('p',{'class':''})[5:]
	rev = []
	i = 0
	for tex in text_list:
		# if not text_list[i].text or  text_list[i].text == extra_string or  text_list[i].text == extra_string2: 
		# 	i-= 1
		if i == 3:
			break
		if not tex.text or tex.text == extra_string:
			continue
		#print i,tex.text
		rev.append(tex.text)
		i += 1
	text_list = rev
	headings =[heading.string for heading in soup.findAll('h2')[:3]]
	authors = soup.findAll('a', {'href':re.compile('user')})[1:6:2]
	authors = [author.string for author in authors]
	reviews = []
	for i in range(count):
		review = {}
		review['index'] = i+1
		review['text'] = text_list[i]
		review['heading'] = headings[i]
		review['author'] = authors[i]
		reviews.append(review)
	#print reviews
	return reviews

def find_movies_by_actor_id(actor_id):
	'''
	Return top 3 movies by an actor 
	using actor_id
	'''
	r = req.get('http://www.imdb.com/name/'+actor_id)
	soup = bs(r.text)
	movie_div = soup.find("div", {"id":"knownfor"})
	if not movie_div:
		return []
	divs = movie_div.findAll("div")
	divs = divs[:3]#To get only Top 3 movies.
	movie_list = []
	for div in divs:
		movie = {}
		url = div.find("a")["href"]
		url = url.split('/')
		movie["movie_id"] = url[2]
		movie["display_pic"],movie["title"],movie["length"],movie["genre"],movie["release_date"],movie["rating"] = get_movie_detail_by_movie_id(movie["movie_id"])
		if movie["rating"] == 'Not Yet Released':
			movie["reviews"] = []
		else:
			movie["reviews"] = get_reviews_by_movie_id(movie["movie_id"])
		movie_list.append(movie)
	return movie_list
		
#find_by_name('shah')
#find_movies_by_actor_id('nm5305841')
#get_reviews_by_movie_id('tt1562872')
#get_movie_detail_by_movie_id('tt4535650')