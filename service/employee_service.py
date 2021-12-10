from app import db
from models.employee import Employee


def employee_by_date(x, y):
    return Employee.query.filter(Employee.date_of_birth <= x.filter(
        Employee.date_of_birth >= y)).all()
