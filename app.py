from datetime import date

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1963@localhost:5432/dep_em'
db = SQLAlchemy(app)


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
        self.employees = employees

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
        return f'Employee: {self.name}, salary: {self.salary}'


def populate_database():
    """
    Populate database with employees and departments
    :return: None
    """
    department_1 = Department('Epam')
    department_2 = Department('SoftServe')
    department_3 = Department('Sombra')

    employee_1 = Employee('Nenchyn Pavlo', 700, date(1996, 5, 12), department_1)
    employee_2 = Employee('Oleh Petryliak', 950, date(1993, 2, 23), department_2)
    employee_3 = Employee('Makam Galant', 700, date(1989, 11, 30), department_3)

    department_1.employees = [employee_1]
    department_2.employees = [employee_2]
    department_3.employees = [employee_3]

    db.session.add(department_1)
    db.session.add(department_2)
    db.session.add(department_3)

    db.session.add(employee_1)
    db.session.add(employee_2)
    db.session.add(employee_3)

    db.session.commit()
    db.session.close()


@app.route('/')
def hello_world():  # put application's code here
    return render_template('departments.html')


if __name__ == '__main__':
    populate_database()
    app.run(debug=True)
