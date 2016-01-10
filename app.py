from flask import Flask, render_template, Response, request, redirect, url_for
from imdb import *
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def homePage():
	actors = []	
	query = request.args.get('query')
	if query is not None and query:
		actors = find_by_name(query)
		#print str(actors)
	return render_template('home.html', actors = actors, query = query)
@app.route('/person/')
@app.route('/person/<actor_id>')
def resultPage(actor_id = None):
	if actor_id:
		name = request.args.get('name')
		if not name:
			return redirect(url_for('homePage'))
		print name
		return render_template('result.html',movies=find_movies_by_actor_id(actor_id),name=name)
	else:
		return redirect(url_for('homePage'))
if __name__=='__main__':
	app.run(debug=True)