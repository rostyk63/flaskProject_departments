from department_app import db
from department_app.models.employee import Employee
from department_app.models.department import Department
from sqlalchemy import desc, asc


def get_department_names() -> list:
    """
    Fetches all department names

    :return: list of department names
    """
    q = db.session.query(Department.name).all()
    result = []
    for t in q:
        for x in t:
            result.append(x)
    return result


def get_all_departments() -> list[Department]:
    """
    Fetches all departments from database

    :return: list of departments
    """
    return Department.query.all()


def get_department_ids() -> list:
    """
    Fetches all department ids

    :return: list of department ids(integers)
    """
    q = db.session.query(Department.id).all()
    result = []
    for t in q:
        for x in t:
            result.append(x)
    return result


def get_amount_of_employees(department_id: str | int) -> int:
    """
    Fetches the number of employees in a particular department by given department_id

    :param department_id: id of department
    :raise TypeError: if department_id is not of type int or str
    :raise ValueError: if department with such id does not exist
    :return: amount of employees(integer)
    """
    if not isinstance(department_id, (int, str)):
        raise TypeError('Department ID should be integer or string.')
    if department_id not in get_department_ids():
        raise ValueError('Invalid department ID')
    return len(db.session.query(Employee).join(Department).filter(Department.id == department_id).all())


def get_avg_salary(department_id: int | str) -> int:
    """
    Fetches the average salary of employees in a particular department by given department_id

    :param department_id: id of department
    :raise TypeError: if department_id is not of type int or str
    :raise ValueError: if department with such id does not exist
    :return: average salary of employees(integer) in department
    """
    if not isinstance(department_id, (int, str)):
        raise TypeError('Department ID should be integer or string.')
    if department_id not in get_department_ids():
        raise ValueError('Invalid department ID')
    if get_amount_of_employees(department_id) == 0:
        return 0
    employees = db.session.query(Employee).join(Department).filter(Department.id == department_id).all()
    return round(sum(map(lambda employee: employee.salary, employees)) / len(employees), 2)


def get_department_by_name(department_name: str) -> list[Department]:
    """
    Fetches the department by given department_name

    :param department_name: name of department
    :raise TypeError: if department_name is not of str type
    :raise ValueError: if department with such name does not exist
    :return: department
    """
    if not isinstance(department_name, str):
        raise TypeError('Department name should be string.')
    if department_name not in get_department_names():
        raise ValueError('Invalid department name')
    return Department.query.filter(Department.name == department_name).all()


def get_department_by_id(department_id: int | str) -> Department:
    """
     Fetches the department by given department_id

    :param department_id: id of department
    :raise TypeError: if department_id is not of type int or str
    :raise ValueError: if department with such id does not exist
    :return: department
    """
    if not isinstance(department_id, (int, str)):
        raise TypeError('Department ID should be integer or string.')
    if department_id not in get_department_ids():
        raise ValueError('Invalid department ID')
    return db.session.query(Department).filter_by(id=department_id).first()


def get_max_salary(department_id: int | str) -> int:
    """
    Fetches max salary of employees in a particular department by given department_id

    :param department_id: id of department
    :raise TypeError: if department_id is not of type int or str
    :raise ValueError: if department with such id does not exist
    :return: max salary(integer) of employees in department
    """
    if not isinstance(department_id, (int, str)):
        raise TypeError('Department ID should be integer or string.')
    if department_id not in get_department_ids():
        raise ValueError('Invalid department ID')
    if get_amount_of_employees(department_id) == 0:
        return 0
    return \
        db.session.query(Employee.salary).filter_by(department_id=department_id).order_by(
            desc(Employee.salary)).first()[0]


def get_min_salary(department_id: int | str) -> int:
    """
    Fetches min salary of employees in a particular department by given department_id

    :param department_id: id of department
    :raise TypeError: if department_id is not of type int or str
    :raise ValueError: if department with such id does not exist
    :return: min salary(integer) of employees in department
    """
    if not isinstance(department_id, (int, str)):
        raise TypeError('Department ID should be integer or string.')
    if department_id not in get_department_ids():
        raise ValueError('Invalid department ID')
    if get_amount_of_employees(department_id) == 0:
        return 0
    return \
        db.session.query(Employee.salary).filter_by(department_id=department_id).order_by(asc(Employee.salary)).first()[
            0]


def get_employees_by_department(department_id: int | str) -> list[Employee]:
    """
    Fetches all employees in a particular department by given department_id

    :param department_id: id of department
    :raise TypeError: if department_id is not of type int or str
    :raise ValueError: if department with such id does not exist
    :return: list of employees
    """
    if not isinstance(department_id, (int, str)):
        raise TypeError('Department ID should be integer or string.')
    if department_id not in get_department_ids():
        raise ValueError('Invalid department ID')
    return db.session.query(Employee).filter_by(department_id=department_id).all()


def update_department_name(department_id: int | str, name: str) -> None:
    """
    Editing department name with given department_id

    :param department_id: id of department
    :param name: new name of department
    :raise TypeError: #1 if department_id is not of type int or str;
                      #2 if name is not of str type
    :raise ValueError: #1 if department with such id does not exist;
                       #2 If department with such name already exists
    :return: None
    """
    if not isinstance(department_id, (int, str)):
        raise TypeError('Department ID should be integer or string.')
    if department_id not in get_department_ids():
        raise ValueError('Invalid department ID.')
    if not isinstance(name, str):
        raise TypeError('Department name should be string.')
    if name in get_department_names():
        raise ValueError('There is already a department with this name.')
    q = db.session.query(Department)
    q = q.filter(Department.id == department_id)
    record = q.one()
    record.name = name
    db.session.commit()


def create_department(name: str) -> None:
    """
    Creating new department

    :param name: name of new department
    :raise TypeError: if name is not of str type
    :raise ValueError: If department with such name already exists
    :return: None
    """
    if not isinstance(name, str):
        raise TypeError('Department name should be string.')
    if name in get_department_names():
        raise ValueError('There is already a department with this name.')
    db.session.add(Department(name))
    db.session.commit()


def add_employee_to_department(name: str, salary: int | str, birthday: str, department: Department) -> None:
    """
    Adding new employee to department by given department

    Example:
    add_employee_to_department('Rostyk', 500, '2002-06-03', get_department_by_id(4))

    :param name: employee name
    :param salary: employee salary
    :param birthday: employee birthday, should be yyyy-mm-dd
    :param department: department
    :return:
    """
    if not department:
        raise ValueError('Invalid department.')
    if not isinstance(name, str):
        raise TypeError('Employee name should be string.')
    if not isinstance(salary, (int, str)):
        raise TypeError('Employee salary should be integer or string.')
    if not isinstance(birthday, str):
        raise TypeError('Employee birthday should be string.')
    db.session.add(Employee(name, salary, birthday, department))
    db.session.commit()


def remove_department(department_id: int | str) -> None:
    """
    Removing department by given department_id

    :param department_id: id of department
    :raise TypeError: if department_id is not of int or str type
    :raise ValueError: if department with such id does not exist
    :return:
    """
    if not isinstance(department_id, (int, str)):
        raise TypeError('Department ID should be integer or string.')
    if department_id not in get_department_ids():
        raise ValueError('Invalid department ID.')
    db.session.query(Employee).filter(Employee.department_id == department_id).delete()
    db.session.query(Department).filter(Department.id == department_id).delete()
    db.session.commit()
