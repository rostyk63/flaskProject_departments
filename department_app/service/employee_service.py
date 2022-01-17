from department_app import db
from department_app.models.employee import Employee
from department_app.models.department import Department


def get_all_employee() -> list[Employee]:
    """
    Fetches all employees from database

    :return: list of employees
    """
    return Employee.query.all()


def get_employee_by_id(employee_id: int) -> Employee:
    """
    Fetches the employee with given id

    :param employee_id: id of employee
    :raise TypeError: if employee_id is not of type int or str
    :raise ValueError: if employee with such id does not exist
    :return: employee
    """
    if not isinstance(employee_id, (int, str)):
        raise TypeError('Employee ID should be integer or string.')
    employee = db.session.query(Employee).filter_by(id=employee_id).first()
    if employee is None:
        raise ValueError('Invalid employee ID')
    return employee


def get_employee_department(department_id: int) -> str:
    """
    Fetches department name of employee with given department_id(Foreign Key of Employee)

    :param department_id: id of employee department
    :raise TypeError: if department_id is not of type int or str
    :raise ValueError: If the Employee.department_id does not exist
    (For example, there is a Department with ID 4, but in the Employee table the department_id(Foreign Key)
     of any employee is not equal to 4)
    :return: employee department
    """
    if not isinstance(department_id, (int, str)):
        raise TypeError('Department ID should be integer or string.')
    employee_department = db.session.query(Employee).filter(Employee.department_id == department_id).first()
    if employee_department is None:
        raise ValueError('Invalid department ID')
    return db.session.query(Department.name).filter(Department.id == department_id).first()[0]


def get_employee_department_id(employee_id: int) -> str:
    """
    Fetches department id of employee with given employee_id

    :param employee_id: id of employee
    :raise TypeError: if employee_id is not of type int or str
    :raise ValueError: if employee with such id does not exist
    :return: employee department id
    """
    if not isinstance(employee_id, (int, str)):
        raise TypeError('Employee ID should be integer or string.')
    employee = db.session.query(Employee).filter_by(id=employee_id).first()
    if employee is None:
        raise ValueError('Invalid employee ID')
    return db.session.query(Employee.department_id).filter(Employee.id == employee_id).first()[0]


def update_employee_name(employee_id: int, name: str) -> None:
    """
    Editing employee name with given employee_id

    :param employee_id: id of employee
    :param name: new name of employee
    :raise TypeError: #1 if employee_id is not of type int or str;
                      #2 if name is not of str type
    :raise ValueError: if employee with such id does not exist
    :return: None
    """
    if not isinstance(employee_id, (int, str)):
        raise TypeError('Employee ID should be integer or string.')
    if not isinstance(name, str):
        raise TypeError('Employee name should be string.')
    employee = db.session.query(Employee).filter_by(id=employee_id).first()
    if employee is None:
        raise ValueError('Invalid employee ID')
    q = db.session.query(Employee)
    q = q.filter(Employee.id == employee_id)
    record = q.one()
    record.name = name
    db.session.commit()


def update_employee_birthday(employee_id: int, birthday: str) -> None:
    """
    Editing employee birthday with given employee_id

    :param employee_id: id of employee
    :param birthday: new birthday of employee, should be yyyy-mm-dd
    :raise TypeError: #1 if employee_id is not of type int or str;
                      #2 if birthday is not of str type
    :raise ValueError: if employee with such id does not exist
    :return: None
    """
    if not isinstance(employee_id, (int, str)):
        raise TypeError('Employee ID should be integer or string.')
    if not isinstance(birthday, str):
        raise TypeError('Employee birthday should be string.')
    employee = db.session.query(Employee).filter_by(id=employee_id).first()
    if employee is None:
        raise ValueError('Invalid employee ID')
    q = db.session.query(Employee)
    q = q.filter(Employee.id == employee_id)
    record = q.one()
    record.date_of_birth = birthday
    db.session.commit()


def update_employee_salary(employee_id: int, salary: int) -> None:
    """
    Editing employee salary with given employee_id

    :param employee_id: id of employee
    :param salary: new salary of employee
    :raise TypeError: #1 if employee_id is not of type int or str;
                      #2 if salary is not of int or str type
    :raise ValueError: if employee with such id does not exist
    :return: None
    """
    if not isinstance(employee_id, (int, str)):
        raise TypeError('Employee ID should be integer or string.')
    if not isinstance(salary, (int, str)):
        raise TypeError('Employee salary should be integer string.')
    employee = db.session.query(Employee).filter_by(id=employee_id).first()
    if employee is None:
        raise ValueError('Invalid employee ID')
    q = db.session.query(Employee)
    q = q.filter(Employee.id == employee_id)
    record = q.one()
    record.salary = salary
    db.session.commit()


def update_employee_department(employee_id: int, department_name: str) -> None:
    """
     Editing employee department with given employee_id

    :param employee_id: id of employee
    :param department_name: new department of employee
    :raise TypeError: #1 if employee_id is not of type int or str;
                      #2 if department_name is not of str type
    :raise ValueError: if employee with such id does not exist
    :return: None
    """
    if not isinstance(employee_id, (int, str)):
        raise TypeError('Employee ID should be integer or string.')
    if not isinstance(department_name, str):
        raise TypeError('Employee department should be string.')
    employee = db.session.query(Employee).filter_by(id=employee_id).first()
    if employee is None:
        raise ValueError('Invalid employee ID')
    q = db.session.query(Employee)
    q = q.filter(Employee.id == employee_id)
    record = q.one()
    record.department_id = db.session.query(Department.id).filter(Department.name == department_name)
    db.session.commit()


def delete_employee(employee_id: int) -> None:
    """
    Removing employee with given employee_id

    :param employee_id: id of employee
    :raise TypeError: if employee_id not of type int or str
    :raise ValueError: if employee with such id does not exist
    :return: None
    """
    if not isinstance(employee_id, (int, str)):
        raise TypeError('Employee ID should be integer or string.')
    employee = db.session.query(Employee).filter_by(id=employee_id).first()
    if employee is None:
        raise ValueError('Invalid employee ID')
    db.session.query(Employee).filter(Employee.id == employee_id).delete()
    db.session.commit()
