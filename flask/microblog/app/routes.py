from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Abey'}
	posts = [
		{
			'author': {'username': 'Abraham'},
			'body': 'Beautiful day in Calicut!'
		},
		{
			'author': {'username': 'Abru'},
			'body': 'The Avengers movie was so cool!'
		}
	]
			
	return render_template('index.html',title='Home',user=user, posts=posts)
