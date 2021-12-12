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


def get_employee_by_id(employee_id):
    """
    Fetches the department with given id
    if there is no such department return None
    :param department_id: id of the department to be fetched
    :return: department with given id or None
    """
    return db.session.query(Employee).filter_by(id=employee_id).first()
