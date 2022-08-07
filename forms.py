from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField, IntegerField
from wtforms.validators import Length, NumberRange, InputRequired


class StudentGradeForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired("Name required"),
                                           Length(min=2, max=25, message="Name must be between 2 and 25 characters")])
    midterm1 = DecimalField('Midterm 1', validators=[InputRequired("Grade required"),
                                                     NumberRange(min=0, max=100, message="Grade must be between 0 and 100")])
    midterm2 = DecimalField('Midterm 2', validators=[InputRequired("Grade required"),
                                                     NumberRange(min=0, max=100, message="Grade must be between 0 and 100")])
    final = DecimalField('Final', validators=[InputRequired("Grade required"),
                                              NumberRange(min=0, max=100, message="Grade must be between 0 and 100")])
    submit = SubmitField('Submit')


class RemoveGradeForm(FlaskForm):
    id = IntegerField('ID', validators=[InputRequired("ID required")])
    submit = SubmitField('Submit')
