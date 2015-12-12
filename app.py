from flask import Flask, render_template, Response, request
from imdb import *
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def showHomePage():
	actors = []	
	query = request.args.get('query')
	if query is not None and query:
		actors = find_by_name(query)
		#print str(actors)
	return render_template('home.html', actors = actors, query = query)

if __name__=='__main__':
	app.run(threaded=True,debug=True)