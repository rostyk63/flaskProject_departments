from app import db


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), unique=True, nullable=False)
    employees = db.relationship(
        'Employee',
        cascade="all,delete",
        backref=db.backref('department', lazy=True),
        lazy=True)

    def __init__(self, name, employees=None):
        self.name = name
        self.employees = employees or []

    def __repr__(self):
        return f'Department name: {self.name} {list(self.employees)}'
