from app import db
from models.employee import Employee
from models.department import Department
from datetime import date
from sqlalchemy import delete


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


def update_employee_name(employee_id, name):
    # update(Employee).where(Employee.id == employee_id).values(name=name)
    # db.session.commit()
    q = db.session.query(Employee)
    q = q.filter(Employee.id == employee_id)
    record = q.one()
    record.name = name

    db.session.commit()


def update_employee_birthday(employee_id, birthday):
    q = db.session.query(Employee)
    q = q.filter(Employee.id == employee_id)
    record = q.one()
    record.date_of_birth = birthday

    db.session.commit()


def update_employee_salary(employee_id, salary):
    q = db.session.query(Employee)
    q = q.filter(Employee.id == employee_id)
    record = q.one()
    record.salary = salary

    db.session.commit()


def update_employee_department(employee_id, department_name):
    q = db.session.query(Employee)
    q = q.filter(Employee.id == employee_id)
    record = q.one()
    record.department_id = db.session.query(Department.id).filter(Department.name == department_name)

    db.session.commit()


def delete_employee(employee_id):
    db.session.query(Employee).filter(Employee.id == employee_id).delete()

    db.session.commit()
