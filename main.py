#Jim Vargas

from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'poop'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


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
        title= existing_blog.title, body= existing_blog.body, id= existing_blog.id)


@app.route("/register", methods=['POST', 'GET'])
def register():
    error = {"name_error": "", "pass_error": "", "verify_error": ""}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if username == "":
            error["name_error"] = "Username cannot be blank"
        if password == "":
            error["pass_error"] = "Password cannot be blank"
        elif len(password) < 2:
            error["pass_error"] = "Password must be more than two characters long"
        else:
            if password != verify:
                error["verify_error"] = "Pasword and Verify must match"

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error["name_error"] = "There is already somebody with that username"

        if error["name_error"] == "" and error["pass_error"] == "" and error["verify_error"] == "":
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/add")
        else:
            return render_template('register.html', title= "Register for this Blog", 
                name_error= error["name_error"], pass_error= error["pass_error"],
                verify_error= error["verify_error"])


    return render_template("register.html", title= "Register for this Blog",
        name_error= error["name_error"], pass_error= error["pass_error"],
        verify_error= error["verify_error"])


if __name__ == '__main__':
    app.run()