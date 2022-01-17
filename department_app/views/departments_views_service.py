from department_app import app
from department_app.service.department_service import *
from flask import flash, request, redirect


def departments_service(form):
    """
    Fetches all departments. Shows Department name and AVG salary.
    Processes the form submission.
     Searches for department by form parameters if at least one of them is filled in by the user.

    :return: departments (name, avg salary, amount of employee, id)
    """
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
    return list(name_salary_employees)


def department_get_service(department_id):
    """
    Fetches a particular department with given id. Shows AVG, min, max salary,
     amount of employees and table of all employees.

    :param department_id: id of department
    :return: department (dict) and employees (dict) in the department
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
    return department_info, employee_infos


def add_employee_service(department_id) -> dict:
    """
    Processes the form submission.
     Validates data and adds employee to the database to department
     from which moved to this page. Flash notification about the success of the operation pops up.

    :param department_id: id of department
    :return: department (dict)
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
    return department_info


def edit_department_service(department_id) -> dict:
    """
    In case of editing department name: Processes the form submission.
     If the department name already exists, a flash notification about the failure of the operation pops up.
     If there is no department name in database, then the name is successfully edited,
     and a flash notification about the success of the operation pops up.

    :param department_id: id of department
    :return: info about edited department
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
    return department_info


def create_department_service():
    """
    If the department name already exists, a flash notification about the failure of the operation pops up.
     If there is no department name in database, it is created in the database and a success notification pops up.

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


def department_name_id(department_id) -> dict:
    """
    Fetches a particular department with given id.

    :param department_id: id of department
    :return: department name and id (dict)
    """
    department = get_department_by_id(department_id)
    app.logger.debug(f'Department data: {department}')
    department_info = {'name': department.name, 'id': department.id}
    return department_info


def department_remove_service(department_id):
    """
    Upon confirmation of the removal of the department, it is deleted from the database

    :param department_id: id of department
    :return: redirects to 'removed_department' page
    """
    app.logger.debug(f"{get_department_by_id(department_id)} is going to be removed")
    remove_department(department_id)
    return redirect('/departments/removed_department')
