from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, IntegerField,SelectField,RadioField, HiddenField
from wtforms.validators import DataRequired,Length, NumberRange,InputRequired
from app import app
from data import card,get_cards,put_cards,card_numbers,get_used_cards,get_unused_cards

# put_cards(card_numbers)

class visitorform(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    purpose = SelectField('Purpose', choices=[
        ('Internship', 'Internship'),
        ('Friends and Family', 'Friends and Family'),
        ('Interview', 'Interview'),
        ('Industry Friends', 'Industry Friends'),
        ('Employee', 'Employee'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    other_purpose = StringField('Other Purpose')
    Card_no = SelectField('Card No', choices=get_unused_cards(),  validate_choice=False)
    submit = SubmitField('Submit')

class exitform(FlaskForm):
    Card_no = SelectField(coerce = int, choices=get_used_cards() , validate_choice=False)
    submit = SubmitField('Submit')

class Feedbackform(FlaskForm):
    category1 = IntegerField('Service_Rating')
    category2 = IntegerField('Quality_Rating')
    category3 = IntegerField('Support_Rating')
    submit = SubmitField('Submit')

class IntroForm(FlaskForm):
    entry = SubmitField('Entry')
    exit = SubmitField('Exit')
    value = HiddenField()
    def set_value(self, button_pressed):
        if button_pressed == 'entry':
            self.value.data = 1
        elif button_pressed == 'exit':
            self.value.data = 2