from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, DateField
from wtforms.validators import Length, NumberRange, Optional


class EmployeeForm(FlaskForm):
    """
    Employee form

    Uses on 'employees' page to search employee
    """
    name = StringField('Name: ',
                       validators=[
                           Length(min=3, max=100, message="Name should be from 3 up to 100 symbols"), Optional()

                       ])
    department = StringField('Department: ',
                             validators=[Length(min=3, max=100, message="Name should be from 3 up to 100 symbols"),
                                         Optional()])
    salary_from = DecimalField('From: ',
                               validators=[NumberRange(min=0, max=100_00, message="Salary should be positive"),
                                           Optional()])
    salary_to = DecimalField('To: ',
                             validators=[NumberRange(min=0, max=100_000, message='Salary should be positive'),
                                         Optional()])
    birth_from = DateField('01.01.1991',
                           validators=[Optional()])
    birth_to = DateField('01.01.2022',
                         validators=[Optional()])
    find = SubmitField('')
