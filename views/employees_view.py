from app import app
from flask import render_template, request
from forms.employee_form import EmployeeForm
from service.employee_service import *


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
