from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import input_required

choices = ['pickup', 'interview', 'product', 'promotion']


class PitchForm(FlaskForm):
    title = StringField('Pitch title', validators=[input_required()])
    pitch = TextAreaField('Text', validators=[input_required()])
    category = SelectField('Type', choices=choices, validators=[input_required()])
    submit = SubmitField('Submit')


class updateProfile(FlaskForm):
    biography= TextAreaField('Tell us about you.', validators=[input_required()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    comment= TextAreaField('Leave a comment:', validators=[input_required()])
    submit = SubmitField('Submit')
