from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1963@localhost:5432/departments'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'fgjknfgjkngdklgoeri'

from forms.department_form import DepartmentForm
from forms.employee_form import EmployeeForm
from service.department_service import *
from service.employee_service import *


@app.route('/', methods=['GET', 'POST'])
@app.route('/departments', methods=['GET', 'POST'])
def departments():
    form = DepartmentForm()
    departments_list = get_all_departments()
    name_salary_employees = [{'name': department.name, 'avg_salary': get_avg_salary(department.id), 'id': department.id,
                              'employee_count': get_amount_of_employee(department.id)} for department in
                             departments_list]
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
        if form.create_name.data:
            create_department(form.create_name.data)
    name_salary_employees = list(name_salary_employees)
    return render_template('departments.html', departments=name_salary_employees, form=form)


@app.route('/employees', methods=['GET', 'POST'])
def employees():
    form = EmployeeForm()
    employees_list = get_all_employee()
    employee_info = [{'name': employee.name, 'department': get_employee_department(employee.department_id)[0][0],
                      'salary': employee.salary, 'date_of_birth': employee.date_of_birth, 'id': employee.id} for
                     employee in
                     employees_list]
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
    employee_info = list(employee_info)
    return render_template('employees.html', employees=employee_info, form=form)


@app.route('/departments/<int:department_id>', methods=['GET', 'POST'])
def department_get(department_id):
    department = get_department_by_id(department_id)
    department_info = {'name': department.name, 'avg_salary': int(get_avg_salary(department.id)),
                       'employee_count': get_amount_of_employee(department.id),
                       'min_salary': get_min_salary(department.id), 'max_salary': get_max_salary(department.id),
                       'id': department.id}
    employees_list = get_employees_by_department(department_id)
    employee_infos = [
        {'name': employee.name, 'salary': employee.salary, 'date_of_birth': employee.date_of_birth, 'id': employee.id}
        for
        employee in
        employees_list]
    return render_template('department.html', department=department_info,
                           employees=employee_infos)


@app.route('/departments/<int:department_id>/add', methods=['GET', 'POST'])
def add_employee(department_id):
    department = get_department_by_id(department_id)
    department_info = {'name': department.name, 'avg_salary': int(get_avg_salary(department.id)),
                       'employee_count': get_amount_of_employee(department.id),
                       'min_salary': get_min_salary(department.id), 'max_salary': get_max_salary(department.id),
                       'id': department.id}
    if request.method == 'POST':
        employee_name = request.form.get('employee_name')
        employee_salary = request.form.get('employee_salary')
        employee_birthday = request.form.get('employee_birthday')
        add_employee_to_department(employee_name, employee_salary, employee_birthday, department)
    return render_template('employee_add.html', department=department_info)


@app.route('/employees/<int:employee_id>', methods=['GET', 'POST'])
def employee_get(employee_id):
    employee = get_employee_by_id(employee_id)
    employee_info = {'name': employee.name, 'salary': employee.salary, 'birthday': employee.date_of_birth,
                     'department': get_employee_department(employee.department_id)[0][0], 'id': employee.id}
    if request.method == 'POST':
        delete_employee(employee_info['id'])
    return render_template('employee.html', employee=employee_info)


@app.route('/employees/<int:employee_id>/edit', methods=['GET', 'POST'])
def edit_employee(employee_id):
    employee = get_employee_by_id(employee_id)
    employee_info = {'name': employee.name, 'salary': employee.salary, 'birthday': employee.date_of_birth,
                     'department': get_employee_department(employee.department_id)[0][0], 'id': employee.id}
    return render_template('employee_add.html', employee=employee_info)


@app.route('/departments/<int:department_id>/edit', methods=['GET', 'POST'])
def edit_department(department_id):
    department = get_department_by_id(department_id)
    department_info = {'name': department.name, 'avg_salary': int(get_avg_salary(department.id)),
                       'employee_count': get_amount_of_employee(department.id),
                       'min_salary': get_min_salary(department.id), 'max_salary': get_max_salary(department.id),
                       'id': department.id}
    if request.method == 'POST':
        department_new_name = request.form.get('department_new_name')
        rename_department(department_info['id'], department_new_name)
    return render_template('department_edit.html', department=department_info)


@app.route('/employees/<int:employee_id>/edit_name', methods=['GET', 'POST'])
def edit_employee_name(employee_id):
    employee = get_employee_by_id(employee_id)
    employee_info = {'name': employee.name, 'salary': employee.salary, 'birthday': employee.date_of_birth,
                     'department': get_employee_department(employee.department_id)[0][0], 'id': employee.id}
    if request.method == 'POST':
        new_name = request.form.get('employee_new_name')
        update_employee_name(employee_info['id'], new_name)
    return render_template('employee_edit_name.html', employee=employee_info)


@app.route('/employees/<int:employee_id>/edit_salary', methods=['GET', 'POST'])
def edit_employee_salary(employee_id):
    employee = get_employee_by_id(employee_id)
    employee_info = {'name': employee.name, 'salary': employee.salary, 'birthday': employee.date_of_birth,
                     'department': get_employee_department(employee.department_id)[0][0], 'id': employee.id}
    if request.method == 'POST':
        new_salary = request.form.get('employee_new_salary')
        update_employee_salary(employee_info['id'], new_salary)
    return render_template('employee_edit_salary.html', employee=employee_info)


@app.route('/employees/<int:employee_id>/edit_birthday', methods=['GET', 'POST'])
def edit_employee_birthday(employee_id):
    employee = get_employee_by_id(employee_id)
    employee_info = {'name': employee.name, 'salary': employee.salary, 'birthday': employee.date_of_birth,
                     'department': get_employee_department(employee.department_id)[0][0], 'id': employee.id}
    if request.method == 'POST':
        new_birthday = request.form.get('employee_new_birthday')
        update_employee_birthday(employee_info['id'], new_birthday)
    return render_template('employee_edit_birthday.html', employee=employee_info)


@app.route('/employees/<int:employee_id>/edit_department', methods=['GET', 'POST'])
def edit_employee_department(employee_id):
    employee = get_employee_by_id(employee_id)
    employee_info = {'name': employee.name, 'salary': employee.salary, 'birthday': employee.date_of_birth,
                     'department': get_employee_department(employee.department_id)[0][0], 'id': employee.id}
    if request.method == 'POST':
        new_department = request.form.get('employee_new_dep')
        update_employee_department(employee_info['id'], new_department)
    return render_template('employee_edit_department.html', employee=employee_info)


if __name__ == '__main__':
    app.run(debug=True)
