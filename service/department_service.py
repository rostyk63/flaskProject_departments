from app import db
from models.employee import Employee
from models.department import Department


def avg_salary_(id_):
    employees1 = db.session.query(Employee).join(Department).filter(Department.id == id_).all()
    try:
        return round(sum(map(lambda employee: employee.salary, employees1)) / len(employees1), 2)
    except ZeroDivisionError:
        return 0


def get_amount_of_employee(id_):
    return len(db.session.query(Employee).join(Department).filter(Department.id == id_).all())


def all_departments():
    return Department.query.all()


def department_by_name(name):
    return Department.query.filter(Department.name == name).all()
