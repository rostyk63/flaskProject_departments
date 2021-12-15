from app import app
from flask import render_template, request
from forms.department_form import DepartmentForm
from service.department_service import *


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
