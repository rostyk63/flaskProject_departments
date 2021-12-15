from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1963@localhost:5432/departments'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'fgjknfgjkngdklgoeri'

from views import departments_view
from views import employees_view
from views import error_view

if __name__ == '__main__':
    app.run(debug=True)
