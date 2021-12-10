from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1963@localhost:5432/departments'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'fgjknfgjkngdklgoeri'

from forms.department_form import DepartmentForm
from forms.employee_form import EmployeeForm
from service.department_service import get_all_departments, get_avg_salary, get_amount_of_employee
from service.employee_service import get_all_employee, get_employee_department


# @app.route('/', methods=['GET', 'POST'])
@app.route('/departments', methods=['GET', 'POST'])
def departments():
    form = DepartmentForm()
    departments_list = get_all_departments()
    name_salary_employees = [{'name': department.name, 'avg_salary': get_avg_salary(department.id),
                              'employee_count': get_amount_of_employee(department.id)} for department in
                             departments_list]
    print(name_salary_employees)
    if form.validate_on_submit():
        if form.name.data:
            name_salary_employees = filter(lambda department: department['name'] == form.name.data,
                                           name_salary_employees)
        if form.min_avg_salary.data:
            name_salary_employees = filter(lambda department: department['avg_salary'] >= form.min_avg_salary.data,
                                           name_salary_employees)
        if form.max_avg_salary.data or form.max_avg_salary.data == 0:
            name_salary_employees = filter(lambda department: department['avg_salary'] <= form.max_avg_salary.data,
                                           name_salary_employees)
        if form.min_employee.data:
            name_salary_employees = filter(lambda department: department['employee_count'] >= form.min_employee.data,
                                           name_salary_employees)
        if form.max_employee.data or form.max_employee.data == 0:
            name_salary_employees = filter(lambda department: department['employee_count'] <= form.max_employee.data,
                                           name_salary_employees)
    name_salary_employees = list(name_salary_employees)
    return render_template('departments.html', departments=name_salary_employees, form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/employees', methods=['GET', 'POST'])
def employees():
    form = EmployeeForm()
    employees_list = get_all_employee()
    employee_info = [{'name': employee.name, 'department': get_employee_department(employee.department_id)[0][0],
                      'salary': employee.salary, 'date_of_birth': employee.date_of_birth} for employee in
                     employees_list]
    print(employee_info)
    if form.validate_on_submit():
        if form.name.data:
            employee_info = filter(lambda employee: employee['name'] == form.name.data, employee_info)
        if form.department.data:
            employee_info = filter(lambda employee: employee['department'] == form.department.data, employee_info)
        if form.salary_from.data:
            employee_info = filter(lambda employee: float(employee['salary']) >= form.salary_from.data, employee_info)
        if form.salary_to.data:
            employee_info = filter(lambda employee: form.salary_to.data >= float(employee['salary']), employee_info)
        if form.birth_from.data:
            employee_info = filter(lambda employee: employee['date_of_birth'] >= form.birth_from.data, employee_info)
        if form.birth_to.data:
            employee_info = filter(lambda employee: employee['date_of_birth'] <= form.birth_to.data, employee_info)
    # form.name.data = ''

    employee_info = list(employee_info)
    return render_template('employees.html', employees=employee_info, form=form)


if __name__ == '__main__':
    app.run(debug=True)
