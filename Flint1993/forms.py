from flask_wtf import FlaskForm #2
from wtforms import StringField,PasswordField,SubmitField
from wtforms.fields.core import SelectField #2
from wtforms.validators import DataRequired,Email #2

class UserLoginForm(FlaskForm):
#email,password,Submit from wtforms
    username=StringField('Username')
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()

#Twitter Mock Form
class ClosetForm(FlaskForm):
    article_category = SelectField('Category',choices=[('Tops','Tops'),('Bottoms','Bottoms'),('Shoes','Shoes')] ,validate_choice=True, validators=[DataRequired()])
    designer=StringField('Designer', validators=[DataRequired()])
    name=StringField('Name', validators=[DataRequired()])
    price=StringField('Price', validators=[DataRequired()])
    image=StringField('Image', validators=[DataRequired()])
    submit_button = SubmitField() #submit
