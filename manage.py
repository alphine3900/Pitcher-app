from typing import Text
from crypt import methods
from enum import unique
from mimetypes import init
from wsgiref.validate import validator
import bcrypt
from .. import db,photos
from flask import Flask, session, render_template,request,redirect,url_for,flash,abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask import PitchForm,CommentForm,updateProfile
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,PasswordField,SubmitField,SelectField
from wtforms.validators import InputRequired,Length,ValidationError
from flask_bcrypt import Bcrypt
from flask import User,Pitch,Comment
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


  class PitchForm(FlaskForm):

   title = StringField('Pitch title',validators=[InputRequired()])
   text = TextAreaField('Text',validators=[InputRequired()])
   category = SelectField('Type',choices=[('interview','Interview pitch'),('product','MOTIVATIONAL pitch'),('promotion','Entertainment pitch')],validators=[InputRequired()])
   submit = SubmitField('Submit')



class updateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators =[ ])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    text = TextAreaField('Leave a comment:',validators=[  ])
    submit = SubmitField('Submit')

@app.route("/")
def home():

    db.create_all()
    if User:
        return render_template("home.html")

    
@app.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    pitches_count = Pitch.count_pitches(uname)
    user_joined = user.date_joined.strftime('%b %d, %Y')

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,pitches = pitches_count,date = user_joined)

@app.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = updateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form = form)

@app.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@app.route('/pitch/new', methods = ['GET','POST'])
@login_required
def new_pitch():
    pitch_form = PitchForm()
    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        pitch = pitch_form.text.data
        category = pitch_form.category.data

        # Updated pitch instance
        new_pitch = Pitch(pitch_title=title,pitch_content=pitch,category=category,user=current_user,likes=0,dislikes=0)

        # Save pitch method
        new_pitch.save_pitch()
        return redirect(url_for('.index'))

    title = 'New pitch'
    return render_template('new_pitch.html',title = title,pitch_form=pitch_form )

@app.route('/pitches/interview_pitches')
def interview_pitches():

    pitches = Pitch.get_pitches('interview')

    return render_template("interview_pitches.html", pitches = pitches)

@app.route('/pitches/product_pitches')
def product_pitches():

    pitches = Pitch.get_pitches('product')

    return render_template("product_pitches.html", pitches = pitches)

@app.route('/pitches/promotion_pitches')
def promotion_pitches():

    pitches = Pitch.get_pitches('promotion')

    return render_template("promotion_pitches.html", pitches = pitches)

@app.route('/pitch/<int:id>', methods = ['GET','POST'])
def pitch(id):
    pitch = Pitch.get_pitch(id)
    posted_date = pitch.posted.strftime('%b %d, %Y')

    if request.args.get("like"):
        pitch.likes = pitch.likes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    elif request.args.get("dislike"):
        pitch.dislikes = pitch.dislikes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data

        new_comment = Comment(comment = comment,user = current_user,pitch_id = pitch)

        new_comment.save_comment()


    comments = Comment.get_comments(pitch)

    return render_template("pitch.html", pitch = pitch, comment_form = comment_form, comments = comments, date = posted_date)

@app.route('/user/<uname>/pitches')
def user_pitches(uname):
    user = User.query.filter_by(username=uname).first()
    pitches = Pitch.query.filter_by(user_id = user.id).all()
    pitches_count = Pitch.count_pitches(uname)
    user_joined = user.date_joined.strftime('%b %d, %Y')

    return render_template("profile/pitches.html", user=user,pitches=pitches,pitches_count=pitches_count,date = user_joined)













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
  title = 'Home - Welcome to  Pitch App'

    # Getting reviews by category
  interview_piches = Pitch.get_pitches('interview')
  product_piches = Pitch.get_pitches('MOTIVATIONAL')
  promotion_pitches = Pitch.get_pitches('Entertainment')


  return render_template('dashboard.html',title = title, interview = interview_piches, product = product_piches, promotion = promotion_pitches)
 

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