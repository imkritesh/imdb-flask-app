import requests as req
from bs4 import BeautifulSoup as bs
import re
import datetime
from multiprocessing import Pool

def find_by_name(name):
	'''
	This function searches IMDB by the name of actor/actress and scrapes 
	necessary data from IMDB and returns an array of dicts.
	Return at maximum top 50 actor/actresses for the search query.
	'''
	r = req.get('http://www.imdb.com/search/name?name='+name)
	soup = bs(r.text, 'html.parser')
	table = soup.find( "div", {"class":"lister-list"})
	# print table
	# return
	#in case of no results
	if not table:
		return []
	rows = table.findAll('div', {"class":"lister-item mode-detail"})
	# print rows[0]
	# return
	query_result = []
	for i, row in enumerate(rows):
		col = {}
		# ro = row.find("td", {"class":"name"})
		# link = ro.find('a')
		
		# name = link.string
		# profile_link = link['href']
		# image_link = row.find('img')["src"]
		# bio = ro.find("span",{"class":"bio"})

		image_div = row.find("div", {"class":"lister-item-image"})
		image_link = image_div.find("img")["src"]
		
		content_div = row.find("div", {"class":"lister-item-content"})
		content_div_header = content_div.find("h3", {"class": "lister-item-header"})
		content_div_header_atag = content_div_header.find("a") 

		name = content_div_header_atag.text
		profile_link = content_div_header_atag["href"]

		bio = content_div.findAll("p")[-1]

		col["name"] = name
		col["actor_id"] = profile_link.split('/')[-1] 
		col["image_link"] = image_link
		if bio is None:
			col["bio"] = ""
		else:
			col["bio"] = bio.text
		query_result.append(col)
	return query_result

def get_movie_detail_by_movie_id(movie_id):
	'''
	This function return movie details
	(display pic, title, length, genre, release_date, rating)
	 of a particular movie. Queries IMDB by movie_id
	'''
	r = req.get('http://www.imdb.com/title/'+movie_id)
	soup = bs(r.text, 'html.parser')
	display = soup.find('div',{'class':'poster'})
	if display:
		display_pic = display.find('a').find('img')['src']
	else:
		display_pic = ''
	infobar = soup.find('div',{'class':'titleBar'})
	title = soup.find('title').string
	title = title.split('-')
	title = '-'.join(title[i] for i in range(len(title)-1)).strip()
	length = infobar.find('time')
	if length:
		length = length.string.strip()
	else:
		length = ''
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
	Returns top 3 reviews of the movie.
	Queries IMDB by movie_id.
	Returns an array of dicts. 
	'''
	extra_string = '*** This review may contain spoilers ***'
	extra_string2 = 'Find showtimes, watch trailers, browse photos, track your Watchlist and rate your favorite movies and TV shows on your phone or tablet!'
	print 'http://www.imdb.com/title/'+movie_id+'/reviews?sort=userRating&dir=desc&ratingFilter=0'
	r = req.get('http://www.imdb.com/title/'+movie_id+'/reviews?sort=userRating&dir=desc&ratingFilter=0')
	soup = bs(r.text, 'html.parser')

	review_containers = soup.findAll("div", {"class":"review-container"})[5:]
	
	reviews = []
	for i, review_container in enumerate(review_containers):
		review = {}
		review['index'] = i + 1
		review['heading'] = review_container.find("div", {"class":"title"}).text
		review['author'] = review_container.find("span", {"class":"display-name-link"}).find("a").text
		review['text'] = review_container.find("div", {"class":"text"}).text
		reviews.append(review)
	
	return reviews

def find_movies_by_actor_id(actor_id):
	'''
	Return top 3 movies by an actor 
	using actor_id
	'''
	pool = Pool()
	pool2 = Pool() 
	startTime = datetime.datetime.now()
	#print 'http://www.imdb.com/name/'+actor_id
	r = req.get('http://www.imdb.com/name/'+actor_id)
	soup = bs(r.text, 'html.parser')
	movie_div = soup.find("div", {"id":"knownfor"})
	if not movie_div:
		return []
	divs = movie_div.findAll("div", {"class":"knownfor-title"})
	divs = divs[:3]#To get only Top 3 movies.
	movie_list = []
	# print divs
	for div in divs:
		movie = {}
		url = div.find("a")["href"]
		url = url.split('/')
		movie["movie_id"] = url[2]
		movie["display_pic"],movie["title"],movie["length"],movie["genre"],movie["release_date"],movie["rating"] = get_movie_detail_by_movie_id(movie["movie_id"])
		#  = pool.apply_async(get_movie_detail_by_movie_id, args = (movie["movie_id"], )).get()
		if movie["rating"] == 'Not Yet Released':
			movie["reviews"] = []
		else:
			movie["reviews"] = get_reviews_by_movie_id(movie["movie_id"])
		movie_list.append(movie)
	endTime = datetime.datetime.now()
	print "Time Taken:", (endTime - startTime).total_seconds()
	return movie_list
		
# print find_by_name('shah')
# print find_movies_by_actor_id('nm0451321')
# print get_reviews_by_movie_id('tt1562872')
# print get_movie_detail_by_movie_id('tt4535650')