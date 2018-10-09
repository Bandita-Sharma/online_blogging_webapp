from flask import Flask,render_template,url_for,redirect,request,session,jsonify,flash
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_disqus import Disqus
import datetime
import re

app=Flask(__name__)
disq=Disqus(app)

app.config['SECRET_KEY'] = 'mysecretkey'

client = MongoClient('mongodb://Bandita:bandita123456789@ds121673.mlab.com:21673/app')
db = client['app']

posts=db.posts
month = {'1':'Jan' , '2':'Feb' , '3':'Mar' , '4':'Apr' , '5':'May' , '6':'Jun','7':'Jul','8':'Aug','9':'Sep','10':'Oct','11':'Nov','12':'Dec'}

@app.route('/',methods=['POST', 'GET'])
def index():
	entertainment = 0
	movies = 0
	technology = 0
	sports = 0
	facts = 0
	others = 0
	find = posts.find()
	blogs = []
	for blog in find:
		blogs.append(blog)
		if blog['tag'] == 'Entertainment':
			entertainment += 1
		elif blog['tag'] == 'Sports':
			sports += 1
		elif blog['tag'] == 'Technology':
			technology += 1
		elif blog['tag'] == 'Facts':
			facts += 1
		elif blog['tag'] == 'Movies':
			movies += 1
		elif blog['tag'] == 'Others':
			others += 1
	tags = {'entertain': entertainment, 'spo': sports, 'tech': technology, 'fact': facts, 'mov': movies, 'oth': others}
	search = []
	while blogs:
		search.append(blogs.pop())
	return render_template('home.html' ,posts=posts, search=search, tags=tags)


@app.route('/admin', methods=['POST','GET'])
def login():
	if request.method == 'POST':
		if request.form['username'] == 'Bandita' and request.form['password'] == 'bandita':
			session['username'] = 'Bandita'
			return redirect(url_for('add_post'))
		else:
			flash('Invalid Username or Password','warning')
			return render_template('login.html')
	return render_template('login.html')

@app.route("/post/<l>", methods=['POST','GET'])
def post(l):
	blog = posts.find_one({"title":str(l)})
	return render_template('post.html', blog=blog)

@app.route('/add_post', methods=['POST','GET'])
def add_post():
	if session['username']:
		a = datetime.date.today()
		date = month[str(a.month)]+" "+str(a.day)+","+str(a.year)
		if request.method == 'POST':
			posts =db.posts
			posts.insert_one({'title':request.form['title'],'content': request.form['content'],'date':date,'image': request.form['image'],'url': request.form['link'],'tag': request.form['tag']})
			flash('Post Added Successfully!','success')
			return render_template('add_post.html')
		return render_template('add_post.html')

	flash('You must login first !!','warning')
	return redirect(url_for('login'))

@app.route('/logout')
def logout():
	session['username'] = None
	return redirect(url_for('login'))

@app.route('/tags/<tag>')
def tags(tag):
	search = posts.find()
	content =[]
	for item in search:
		if item['tag'] == tag:
			content.append(item)
	return render_template('tag.html', content=content)

@app.route('/<dt>')
def date(dt):
	content =[]
	search = posts.find()
	for item in search:
		if item['date'] == dt:
			content.append(item)
	return render_template('date.html', content=content)

@app.route('/search/', methods=['POST','GET'])
def search():
	if request.method == 'POST':
		data = request.form['search']
		a = re.compile(str(request.form['search']), re.IGNORECASE)
		search = posts.find()
		content = []
		for item in search:
			b = a.findall(item['title'])
			for j in b:
				content.append(item)
		return render_template('tag.html', content=content)
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True)
