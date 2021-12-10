from app import db
from models.employee import Employee
from models.department import Department


def get_employee_by_date(x, y):
    return Employee.query.filter(Employee.date_of_birth <= x.filter(
        Employee.date_of_birth >= y)).all()


def get_all_employee():
    return Employee.query.all()


def get_employee_department(department_id):
    return db.session.query(Department.name).filter(Department.id == department_id).all()

