#Jim Vargas

from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'poop'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route("/")
def index():
    return redirect("/blog")


@app.route("/blog")
def home():
    blogs = Blog.query.all()

    return render_template('home.html', title= "Build A Blog", blogs= blogs)


@app.route("/add", methods= ['POST', 'GET'])
def AddBlog():
    error = {"title_blank": "", "body_blank": ""}
    new_body = ""
    new_title = ""
    if request.method == 'POST':
        new_title = request.form["title"]
        new_body = request.form["body"]

        if new_title == "":
            error["title_blank"] = "Enter a title for your blog"
        if new_body == "":
            error["body_blank"] = "Enter some text for your blog's body"

        if error["title_blank"] == "" and error["body_blank"] == "":
            new_blog = Blog(new_title, new_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/individual?blog_title="+new_title)
        else:
            return render_template('add.html', title= "Add a blog post", 
                add_body= new_body, add_title= new_title,
                title_blank= error["title_blank"], body_blank= error["body_blank"])
    
    return render_template('add.html', title= "Add a blog post", 
        add_body= new_body, add_title= new_title,
        title_blank= error["title_blank"], body_blank= error["body_blank"])


@app.route("/individual")
def OneBlog():
    title = request.args.get('blog_title')
    existing_blog = Blog.query.filter_by(title= title).first()

    return render_template("individual.html", 
        title= existing_blog.title, body= existing_blog.body)


if __name__ == '__main__':
    app.run()