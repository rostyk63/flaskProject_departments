from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import Length, NumberRange, Optional


class DepartmentForm(FlaskForm):
    """
    Department form
    """
    name = StringField('Name: ',
                       validators=[
                           Length(min=3, max=100,
                                  message="Name should be from 3 up to 100 symbols"), Optional()])
    min_avg_salary = DecimalField('Min avg salary: ',
                                  validators=[NumberRange(min=0, max=100_000, message='Salary should be positive'),
                                              Optional()])
    max_avg_salary = DecimalField('Max avg salary: ',
                                  validators=[
                                      NumberRange(min=0, max=100_000, message='Salary should be positive'), Optional()])
    min_employee = DecimalField('Min amount of employee: ',
                                validators=[
                                    NumberRange(min=0, max=100_000, message='Amount of employee should be positive'), ])
    max_employee = DecimalField('Max amount of employee: ',
                                validators=[
                                    NumberRange(min=0, max=100_000, message='Amount of employee should be positive'), ])
    find = SubmitField('')
