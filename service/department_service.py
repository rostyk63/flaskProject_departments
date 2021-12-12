from app import db
from models.employee import Employee
from models.department import Department
from sqlalchemy import desc, asc


def get_avg_salary(department_id):
    employees = db.session.query(Employee).join(Department).filter(Department.id == department_id).all()
    try:
        return round(sum(map(lambda employee: employee.salary, employees)) / len(employees), 2)
    except ZeroDivisionError:
        return 0


def get_amount_of_employee(department_id):
    return len(db.session.query(Employee).join(Department).filter(Department.id == department_id).all())


def get_all_departments():
    return Department.query.all()


def get_department_by_name(department_name):
    return Department.query.filter(Department.name == department_name).all()


def get_department_by_id(department_id):
    """
    Fetches the department with given id
    if there is no such department return None
    :param department_id: id of the department to be fetched
    :return: department with given id or None
    """
    return db.session.query(Department).filter_by(id=department_id).first()


def get_min_salary(department_id):
    return \
        db.session.query(Employee.salary).filter_by(department_id=department_id).order_by(
            desc(Employee.salary)).first()[0]


def get_max_salary(department_id):
    return \
        db.session.query(Employee.salary).filter_by(department_id=department_id).order_by(asc(Employee.salary)).first()[
            0]


def get_employees_by_department(department_id):
    return db.session.query(Employee).filter_by(department_id=department_id).all()
