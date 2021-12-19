from department_app import db


class Employee(db.Model):
    """
    Model representing employee

    ...

    Attributes
    __________
    name : str
        name of employee
    salary : int
        salary of employee
    date_of_birth : date
        employee birthday
    department : Department or None
        department employee works in
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(55), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    def __init__(self, name, salary, date_of_birth, department):
        self.name = name
        self.salary = salary
        self.date_of_birth = date_of_birth
        self.department = department

    def __repr__(self):
        """
        returns string representation of employee

        :return: employee
        """
        return f'Employee: {self.name}, salary: {self.salary}, birth: {self.date_of_birth}'
