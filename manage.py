
from crypt import methods
from flask import Flask, session, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://moringa:Access@localhost/alphine"
app.config["SECRET_KEY"] = "thisisasecretkey"


class User(db.model):
  id = db.Column(db.Integer,primary_key=True)
  User = db.Column(db.string(20), nullable=false)
  completed = db.Column(db.integer,default=0)


@app.route('/',methods = ["GET","POST"])
def home():

  if request.method == "POST":
        session.pop ("user",None)

        if request.form["password"] == "password":
            session["user"] = request.form["username"]
            return redirect(url_for("register"))

  return render_template('home.html')



@app.route("/register")
def register():
    if g.user:
        return render_template("protected.html",user=session["user"])
        return redirect(url_for("register.html"))


@app.before_request
def before_request():

    if g.user == None

    if "user" in session:
        g.user = session["user"]

    return render_template("home.html")



@app.route('/register')
def register():
  return render_template('register.html')

@app.route('/login')
def login():
  return render_template('login.html')


if __name__ == '__main__':
     app.run(debug = True) 