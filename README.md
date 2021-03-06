# imdb-flask-app

A flask web-app in which user searches actor/actress by name and the application performs a search on IMDb, scrapes top 3 movies of the actor/actress, each with the top 3 user reviews (most helpful) of the movie and lists the results in tabular format.

# How to Run?
1. Create virtualenv and install dependencies
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```
2. To run
```
python app.py
```
3. Visit http://localhost:5000/

# Screenshots
- Index Page
![Index Page](screenshots/index.png "Index Page")
- Result Page
![Result Page](screenshots/result.png "Result Page")

