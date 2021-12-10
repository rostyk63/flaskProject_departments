from datetime import date

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from sqlalchemy import and_, func, desc, asc

app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1963@localhost:5432/departments'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'fgjknfgjkngdklgoeri'


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), unique=True, nullable=False)
    employees = db.relationship(
        'Employee',
        cascade="all,delete",
        backref=db.backref('department', lazy=True),
        lazy=True)

    def __init__(self, name, employees=None):
        self.name = name
        self.employees = employees or []

    def __repr__(self):
        return f'Department name: {self.name} {list(self.employees)}'


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(55), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    def __init__(self, name, salary, date_of_birth, department):
        self.name = name
        self.salary = salary
        self.date_of_birth = date_of_birth
        self.department = department

    def __repr__(self):
        return f'Employee: {self.name}, salary: {self.salary}, birth: {self.date_of_birth}'


def populate_database():
    """
    Populate database with employees and departments
    :return: None
    """
    db.drop_all()
    db.create_all()
    department_1 = Department('Epam')
    department_2 = Department('SoftServe')
    department_3 = Department('Sombra')

    employee_1 = Employee('Nenchyn Pavlo', 700, date(2002, 8, 22), department_1)
    employee_2 = Employee('Oleh Petryliak', 950, date(2002, 10, 4), department_2)
    employee_3 = Employee('Makam Galant', 700, date(1989, 11, 25), department_3)

    db.session.add(department_1)
    db.session.add(department_2)
    db.session.add(department_3)

    db.session.add(employee_1)
    db.session.add(employee_2)
    db.session.add(employee_3)

    db.session.commit()
    db.session.close()


def avg_salary_(id_):
    employees1 = db.session.query(Employee).join(Department).filter(Department.id == id_).all()
    try:
        return round(sum(map(lambda employee: employee.salary, employees1)) / len(employees1), 2)
    except ZeroDivisionError:
        return 0


def get_amount_of_employee(id_):
    return len(db.session.query(Employee).join(Department).filter(Department.id == id_).all())


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class DepartmentForm(FlaskForm):
    """
    Department form
    """
    name = StringField('Name: ',
                       validators=[
                           Length(min=3, max=100,
                                  message="Name should be from 3 up to 100 symbols"),
                           Optional()
                           # DataRequired()
                       ])
    min_avg_salary = DecimalField('Salary: ',
                                  validators=[
                                      NumberRange(min=0, max=100_000, message='Salary should be positive'),
                                      Optional()
                                      # DataRequired()
                                  ])
    max_avg_salary = DecimalField('Salary: ',
                                  validators=[
                                      NumberRange(min=0, max=100_000, message='Salary should be positive'),
                                      Optional()
                                      # DataRequired()
                                  ])
    min_employee = DecimalField('Salary: ',
                                validators=[
                                    NumberRange(min=0, max=100_000, message='Salary should be positive'),
                                    Optional()
                                    # DataRequired()
                                ])
    max_employee = DecimalField('Salary: ',
                                validators=[
                                    NumberRange(min=0, max=100_000, message='Salary should be positive'),
                                    Optional()
                                    # DataRequired()
                                ])
    submit = SubmitField('')


@app.route('/', methods=['GET', 'POST'])
@app.route('/departments', methods=['GET', 'POST'])
def departments():  # put application's code here
    form = DepartmentForm()
    departments_list = Department.query.all()
    departments_ = [{'name': department.name, 'avg_salary': avg_salary_(department.id),
                     'employee_count': get_amount_of_employee(department.id)} for department in
                    departments_list]
    if form.validate_on_submit():
        if form.name.data:
            departments_ = filter(lambda department: department['name'] == form.name.data, departments_)
        if form.min_avg_salary.data:
            departments_ = filter(lambda department: department['avg_salary'] >= form.min_avg_salary.data, departments_)
        if form.max_avg_salary.data or form.max_avg_salary.data == 0:
            departments_ = filter(lambda department: department['avg_salary'] <= form.max_avg_salary.data, departments_)
        if form.min_employee.data:
            departments_ = filter(lambda department: department['employee_count'] >= form.min_employee.data,
                                  departments_)
        if form.max_employee.data or form.max_employee.data == 0:
            departments_ = filter(lambda department: department['employee_count'] <= form.max_employee.data,
                                  departments_)
    departments_ = list(departments_)
    print(departments_)
    return render_template('departments.html', departments=departments_, form=form)  # , departments=departments)


@app.route('/employees')
def employees():
    return render_template('employees.html')


# populate_database()
def all_departments():
    return Department.query.all()


def employee_by_date(x, y):
    return Employee.query.filter(Employee.date_of_birth <= x.filter(
        Employee.date_of_birth >= y)).all()


def department_by_name(name):
    return Department.query.filter(Department.name == name).all()


if __name__ == '__main__':
    app.run(debug=True)
