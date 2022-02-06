from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false
# from flask_login import UserMixim

app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://moringa:Access@localhost/alphine"
app.config["SECRET_KEY"] = "thisisasecretkey"


class User(db.model):
  id = db.Column(db.Integer,primary_key=True)
  User = db.Column(db.string(20), nullable=false)
  password = db.Column(db.string(80), nullable=false)


@app.route('/')
def home():
  return render_template('home.html')



@app.route('/register')
def register():
  return render_template('register.html')

@app.route('/login')
def login():
  return render_template('login.html')


if __name__ == '__main__':
     app.run(debug = True) 