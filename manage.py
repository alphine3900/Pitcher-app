
from crypt import methods
from flask import Flask, session, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://moringa:Access@localhost/alphine"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"] = "thisisasecretkey"


class User(db.Model):
  id = db.Column(db.Integer,primary_key=True)
  User = db.Column(db.String(20), nullable=False)
  completed = db.Column(db.Integer,default=0)


@app.route('/login',methods = ["GET","POST"])
def login():

  if request.method == "POST":
        session.pop ("user",None)

        if request.form["password"] == "password":
            session["user"] = request.form["username"]
            return redirect(url_for("home"))

  return render_template('login.html')




@app.route("/register")
def register():
    if User:
        return render_template("register.html")
        return redirect(url_for("home"))




@app.route("/")
def home():
    if User:
        return render_template("home.html")
        return redirect(url_for("register"))


@app.before_request
def before_request():

    if User == None:

     if "user" in session:
        user = session["user"]

    return render_template("login.html")
    return redirect(url_for("home"))



# @app.route('/register')
# def register():
#   return render_template('register.html')

# @app.route('/login')
# def login():
#   return render_template('login.html')


if __name__ == '__main__':
     app.run(debug = True) 