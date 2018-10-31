#import
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy #..데이터베이스
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/sola/Desktop/Cleanblog/blog.db'
db = SQLAlchemy(app)

#데이터베이스 칼럼 만들기
class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

#page route
@app.route('/')
def index():
    
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    
    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())
    
    #db에 데이터 추가하기
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id = post_id).one()

    return render_template('post.html',post=post)

#앱 실행
if __name__=='__main__':
    app.run(debug=True)