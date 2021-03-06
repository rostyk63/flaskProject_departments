from department_app import db
from department_app.models.department import Department
from department_app.models.employee import Employee
from datetime import date


def populate_database():
    db.drop_all()
    db.create_all()
    department_1 = Department('Epam')
    department_2 = Department('SoftServe')
    department_3 = Department('Sombra')
    department_4 = Department('GlobalLogic')
    department_5 = Department('Incora')
    department_6 = Department('SerVer')

    employee_1 = Employee('Nenchyn Pavlo', 700, date(2002, 8, 22), department_1)
    employee_2 = Employee('Petryliak Oleh', 950, date(2002, 10, 4), department_2)
    employee_3 = Employee('Galant Makam', 700, date(1989, 11, 25), department_3)
    employee_4 = Employee('Dmytrasevych Iryna', 5000, date(2002, 6, 5), department_4)
    employee_5 = Employee('Ihor Sohan Molodets', 299, date(2002, 1, 1), department_5)
    employee_6 = Employee('Patsay Vladyslav', 100, date(2002, 10, 3), department_1)
    employee_7 = Employee('Halik OleksandOr', 55, date(1989, 7, 1), department_1)
    employee_8 = Employee('Pasichnyk Noname', 10, date(2002, 6, 5), department_6)

    db.session.add(department_1)
    db.session.add(department_2)
    db.session.add(department_3)
    db.session.add(department_4)
    db.session.add(department_5)
    db.session.add(department_6)

    db.session.add(employee_1)
    db.session.add(employee_2)
    db.session.add(employee_3)
    db.session.add(employee_4)
    db.session.add(employee_5)
    db.session.add(employee_6)
    db.session.add(employee_7)
    db.session.add(employee_8)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    populate_database()
