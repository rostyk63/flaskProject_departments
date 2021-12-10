from app import db
from models.employee import Employee
from models.department import Department


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
