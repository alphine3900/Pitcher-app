
from crypt import methods
from enum import unique
from mimetypes import init
from wsgiref.validate import validator
import bcrypt
from flask import Flask, session, render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length,ValidationError
from flask_bcrypt import Bcrypt
from databases import Database
# from app import db


app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://moringa:alphine@localhost/register"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"] = "thisisasecretkey"



login_manager=LoginManager()
login_manager.init_app(app)
login_manager.view_login="login"


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(init(user_id))

class User(db.Model,UserMixin):
  __tablename__="users"
  id = db.Column(db.Integer,primary_key=True)
  username = db.Column(db.String(50), nullable=False, unique=True)
  # email = db.Column(db.String(50), nullable=False)
  password = db.Column(db.String(200),nullable=False)


class RegisterForm(FlaskForm):
  username=StringField(validators=[InputRequired(),Length(min=4, max=20) ], render_kw={"placeholder":"username"})


  password=StringField(validators=[InputRequired(),Length(min=4, max=20) ], render_kw={"placeholder":"password"})
  submit=SubmitField("Register")

  # email=StringField(validators=[InputRequired(),Length(min=4, max=200) ], render_kw={"placeholder":"email"})
  # submit=SubmitField("Register")


  def validate_username(self,username):
    existing_user_username=User.query.filter_by(username=username.data).first()
    if existing_user_username:
      raise ValidationError("This username already exist,please choose a different one")


class LoginForm(FlaskForm):
  username=StringField(validators=[InputRequired(),Length(min=4, max=20) ], render_kw={"placeholder":"username"})


  password=StringField(validators=[InputRequired(),Length(min=4, max=20) ], render_kw={"placeholder":"password"})
  submit=SubmitField("Login")

@app.route("/")
def home():
    db.create_all()
    if User:
        return render_template("home.html")





@app.route('/login', methods=["GET","POST"])
def login():
  form=LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by (username=form.username.data).first()
    if user:
      # if bcrypt.check_password_hash(user.password,form.password.data):
      #   login_user(user)
     if user.check_password_hash(user.password,form.password.data):

            login_user(user)
            flash('Logged in Succesfully!')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('')

            # return redirect(next)
    return redirect(url_for("dashboard"))

  
  return render_template('dashboard.html', form=form)



@app.route('/dashboard')
@login_required
def dashboard():
 

  return render_template('dashboard.html')


@app.route('/pitches', methods=["GET","POST"])
# @login_required
def pitches():
 

  return render_template('pitches.html')




app.route('/logout', methods=["GET","POST"])
@login_required
def logout():
  logout_user()
  return redirect(url_for("home"))
 




@app.route("/register", methods=["GET","POST"])
def register():
  form=RegisterForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data)
    new_user=User(username=form.password.data, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash("Thanks for registration!")
    return redirect(url_for("login"))
    
  return render_template("register.html", form=form)
 
        


if __name__ == '__main__':
     app.run(debug = True) 