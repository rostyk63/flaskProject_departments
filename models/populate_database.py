from app import db
from models.department import Department
from models.employee import Employee
from datetime import date


def populate_database():
    """
    Populate database with employees and departments
    :return: None
    """
    db.drop_all()
    db.create_all()
    department_1 = Department('Epam')
    department_2 = Department('SoftServe')
    department_3 = Department('Sombra')
    department_4 = Department('GlobalLogic')

    employee_1 = Employee('Nenchyn Pavlo', 700, date(2002, 8, 22), department_1)
    employee_2 = Employee('Petryliak Oleh', 950, date(2002, 10, 4), department_2)
    employee_3 = Employee('Galant Makam', 700, date(1989, 11, 25), department_3)
    employee_4 = Employee('Dmytrasevych Iryna', 5000, date(2002, 6, 5), department_4)

    db.session.add(department_1)
    db.session.add(department_2)
    db.session.add(department_3)
    db.session.add(department_4)

    db.session.add(employee_1)
    db.session.add(employee_2)
    db.session.add(employee_3)
    db.session.add(employee_4)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    populate_database()
