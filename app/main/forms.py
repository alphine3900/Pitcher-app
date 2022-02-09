from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import InputRequired

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