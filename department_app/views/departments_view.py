from department_app import app
from flask import render_template, request, flash, redirect
from department_app.forms.department_form import DepartmentForm
from department_app.service.department_service import *


@app.route('/', methods=['GET'])
def main_page():
    """
    Renders 'main_page.html' template.
    Depending on the choice of the user redirects to 'departments' page or 'employees' page.

    :return: rendered 'main_page.html' template
    """
    app.logger.debug('main_page.html was rendered')
    return render_template('main_page.html')


@app.route('/departments', methods=['GET', 'POST'])
def departments():
    """
    Fetches all departments. Shows Department name and AVG salary.
    Renders 'departments.html' template.
    Processes the form submission.
     Searches for department by form parameters if at least one of them is filled in by the user.
    Redirects to 'create' page in case of creating a department.
    Redirects to 'department_get' page in case of view of a particular department.

    :return: rendered 'departments.html' template
    """
    form = DepartmentForm()
    departments_list = get_all_departments()
    app.logger.debug(f'Departments: {departments_list}')
    name_salary_employees = [{'name': department.name, 'avg_salary': get_avg_salary(department.id), 'id': department.id,
                              'employee_count': get_amount_of_employees(department.id)} for department in
                             departments_list]
    if form.validate_on_submit():
        app.logger.debug('Searching for department using Form')
        if form.name.data:
            name_salary_employees = filter(lambda department: department['name'] == form.name.data,
                                           name_salary_employees)
            app.logger.debug(f'Form data department name: {form.name.data}')
        if form.min_avg_salary.data:
            name_salary_employees = filter(lambda department: department['avg_salary'] >= form.min_avg_salary.data,
                                           name_salary_employees)
            app.logger.debug(f'Form data min avg salary: {form.min_avg_salary.data}')
        if form.max_avg_salary.data or form.max_avg_salary.data == 0:
            name_salary_employees = filter(lambda department: department['avg_salary'] <= form.max_avg_salary.data,
                                           name_salary_employees)
            app.logger.debug(f'Form data max avg salary: {form.max_avg_salary.data}')
        if form.min_employee.data:
            name_salary_employees = filter(lambda department: department['employee_count'] >= form.min_employee.data,
                                           name_salary_employees)
            app.logger.debug(f'Form data min amount of employee: {form.min_employee.data}')
        if form.max_employee.data or form.max_employee.data == 0:
            name_salary_employees = filter(lambda department: department['employee_count'] <= form.max_employee.data,
                                           name_salary_employees)
            app.logger.debug(f'Form data max amount of employee: {form.max_employee.data}')
    name_salary_employees = list(name_salary_employees)
    app.logger.debug('departments.html was rendered')
    return render_template('departments.html', departments=name_salary_employees, form=form)


@app.route('/departments/<int:department_id>', methods=['GET', 'POST'])
def department_get(department_id):
    """
    Fetches a particular department with given id. Shows AVG, min, max salary,
     amount of employees and table of all employees.
    Renders 'department.html' template.
    Redirects to 'add_employee' page in case of adding new employee to department.
    Redirects to 'edit_department' page in case of editing department.

    :param department_id: id of department
    :return: rendered 'department.html' template
    """
    department = get_department_by_id(department_id)
    app.logger.debug(f'Department data: {department}')
    department_info = {'name': department.name, 'avg_salary': int(get_avg_salary(department.id)),
                       'employee_count': get_amount_of_employees(department.id),
                       'min_salary': get_min_salary(department.id), 'max_salary': get_max_salary(department.id),
                       'id': department.id}
    employees_list = get_employees_by_department(department_id)
    employee_infos = [
        {'name': employee.name, 'salary': employee.salary, 'date_of_birth': employee.date_of_birth, 'id': employee.id}
        for
        employee in
        employees_list]
    app.logger.debug(f'Employees data: {employees_list}')
    app.logger.debug('department.html was rendered')
    return render_template('department.html', department=department_info,
                           employees=employee_infos)


@app.route('/departments/<int:department_id>/add', methods=['GET', 'POST'])
def add_employee(department_id):
    """
    Renders 'employee_add.html' template.
    Processes the form submission.
     Validates data and adds employee to the database to department
     from which moved to this page. Flash notification about the success of the operation pops up.

    :param department_id: id of department
    :return: rendered 'employee_add.html' template
    """
    department = get_department_by_id(department_id)
    app.logger.debug(f'Department data: {department}')
    department_info = {'name': department.name, 'avg_salary': int(get_avg_salary(department.id)),
                       'employee_count': get_amount_of_employees(department.id),
                       'min_salary': get_min_salary(department.id), 'max_salary': get_max_salary(department.id),
                       'id': department.id}
    if request.method == 'POST':
        employee_name = request.form.get('employee_name')
        employee_salary = request.form.get('employee_salary')
        employee_birthday = request.form.get('employee_birthday')
        add_employee_to_department(employee_name, employee_salary, employee_birthday, department)
        flash('The employee was successfully added.', category='success')
        app.logger.debug(f'New employee: {employee_name}, salary: {employee_salary}, birthday {employee_birthday}')
    app.logger.debug('employee_add.html was rendered')
    return render_template('employee_add.html', department=department_info)


@app.route('/departments/<int:department_id>/edit', methods=['GET', 'POST'])
def edit_department(department_id):
    """
    Renders 'department_edit.html' template
    In case of editing department name: Processes the form submission.
     If the department name already exists, a flash notification about the failure of the operation pops up.
     If there is no department name in database, then the name is successfully edited,
     and a flash notification about the success of the operation pops up.
    Redirects to 'department_remove' when trying to remove department.

    :param department_id: id of department
    :return: rendered 'department_edit.html' template
    """
    department = get_department_by_id(department_id)
    app.logger.debug(f'Department data: {department}')
    department_info = {'name': department.name, 'avg_salary': int(get_avg_salary(department.id)),
                       'employee_count': get_amount_of_employees(department.id),
                       'min_salary': get_min_salary(department.id), 'max_salary': get_max_salary(department.id),
                       'id': department.id}
    if request.method == 'POST':
        department_new_name = request.form.get('department_new_name')
        if department_new_name not in get_department_names():
            update_department_name(department_info['id'], department_new_name)
            flash('The name of the department was successfully edited.', category='success')
            app.logger.debug(f'New department name data: {department_new_name}')
        else:
            flash('There is already a department with this name.', category='error')
            app.logger.debug(f'Invalid data: {department_new_name}')
    app.logger.debug('department_edit.html was rendered')
    return render_template('department_edit.html', department=department_info)


@app.route('/departments/create_department', methods=['GET', 'POST'])
def create():
    """
    Renders 'department_create.html' template
    If the department name already exists, a flash notification about the failure of the operation pops up.
     If there is no department name in database, it is created in the database and a success notification pops up.

    :return: rendered 'department_create.html' template
    """
    app.logger.debug('New department is going to be created')
    if request.method == 'POST':
        name = request.form.get('name')
        if name not in get_department_names():
            create_department(name)
            flash('The department was successfully created.', category='success')
            app.logger.debug(f'New department data: {name}')
        else:
            flash('There is already a department with this name.', category='error')
            app.logger.debug(f'Invalid data: {name}')
    app.logger.debug('department_create.html was rendered')
    return render_template('department_create.html')


@app.route('/departments/<int:department_id>/remove', methods=['GET', 'POST'])
def department_remove(department_id):
    """
    Renders 'department_remove.html' template.
    Upon confirmation of the removal of the department, it is deleted from the database,
    redirects to 'removed_department' page.

    :param department_id: id of department
    :return: rendered 'department_remove.html' template
    """
    department = get_department_by_id(department_id)
    app.logger.debug(f'Department data: {department}')
    department_info = {'name': department.name, 'id': department.id}
    if request.method == 'POST':
        app.logger.debug(f"{get_department_by_id(department_id)} is going to be removed")
        remove_department(department_id)
        # app.logger.debug(f"Department {get_department_by_id(department_id)} is going to be removed")
        return redirect('/departments/removed_department')
    app.logger.debug(f'department_remove.html was rendered')
    return render_template('department_remove.html', department=department_info)


@app.route('/departments/removed_department', methods=['GET'])
def removed_department():
    """
    Renders 'removed_department.html' template.
    A flash notification about the success of the operation pops up.
    Arrow back redirects on 'departments' page.

    :return: rendered 'removed_department.html' template
    """
    app.logger.debug('Department was removed')
    flash('The department was successfully removed.', category='success')
    app.logger.debug('removed_department.html was rendered')
    return render_template('removed_department.html')
