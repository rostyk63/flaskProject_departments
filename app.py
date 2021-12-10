from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1963@localhost:5432/departments'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'fgjknfgjkngdklgoeri'

from forms.department_form import DepartmentForm
from models.department import Department
from models.employee import Employee
from service.department_service import avg_salary_, get_amount_of_employee


@app.route('/', methods=['GET', 'POST'])
@app.route('/departments', methods=['GET', 'POST'])
def departments():
    form = DepartmentForm()
    departments_list = Department.query.all()
    departments_ = [{'name': department.name, 'avg_salary': avg_salary_(department.id),
                     'employee_count': get_amount_of_employee(department.id)} for department in
                    departments_list]
    if form.validate_on_submit():
        if form.name.data:
            departments_ = filter(lambda department: department['name'] == form.name.data, departments_)
        if form.min_avg_salary.data:
            departments_ = filter(lambda department: department['avg_salary'] >= form.min_avg_salary.data, departments_)
        if form.max_avg_salary.data or form.max_avg_salary.data == 0:
            departments_ = filter(lambda department: department['avg_salary'] <= form.max_avg_salary.data, departments_)
        if form.min_employee.data:
            departments_ = filter(lambda department: department['employee_count'] >= form.min_employee.data,
                                  departments_)
        if form.max_employee.data or form.max_employee.data == 0:
            departments_ = filter(lambda department: department['employee_count'] <= form.max_employee.data,
                                  departments_)
    departments_ = list(departments_)
    print(departments_)
    return render_template('departments.html', departments=departments_, form=form)


@app.route('/employees')
def employees():
    return render_template('employees.html')


if __name__ == '__main__':
    app.run(debug=True)
