from department_app import app
from department_app.service.employee_service import *
from flask import flash, request, redirect
from department_app.service.department_service import get_department_names


def employees_service(form):
    """
    Fetches all employees. Shows employee name, department, salary and birthday.
    Processes the form submission.
     Searches for employee by form parameters if at least one of them is filled in by the user.

    :return: employees(name, department, salary, birthday, id)
    """
    employees_list = get_all_employee()
    app.logger.debug(f'Employees data: {employees_list}')
    employee_info = [{'name': employee.name, 'department': get_employee_department(employee.department_id),
                      'salary': employee.salary, 'date_of_birth': employee.date_of_birth, 'id': employee.id} for
                     employee in
                     employees_list]
    if form.validate_on_submit():
        app.logger.debug('Searching for employee using Form')
        if form.name.data:
            employee_info = filter(lambda employee: employee['name'] == form.name.data, employee_info)
            app.logger.debug(f'Form data employee name: {form.name.data}')
        if form.department.data:
            employee_info = filter(lambda employee: employee['department'] == form.department.data, employee_info)
            app.logger.debug(f'Form data employee department: {form.department.data}')
        if form.salary_from.data:
            employee_info = filter(lambda employee: int(employee['salary']) >= form.salary_from.data, employee_info)
            app.logger.debug(f'Form data employee salary from: {form.salary_from.data}')
        if form.salary_to.data:
            employee_info = filter(lambda employee: form.salary_to.data >= int(employee['salary']), employee_info)
            app.logger.debug(f'Form data employee salary to: {form.salary_to.data}')
        if form.birth_from.data:
            employee_info = filter(lambda employee: employee['date_of_birth'] >= form.birth_from.data, employee_info)
            app.logger.debug(f'Form data employee birthday from: {form.birth_from.data}')
        if form.birth_to.data:
            employee_info = filter(lambda employee: employee['date_of_birth'] <= form.birth_to.data, employee_info)
            app.logger.debug(f'Form data employee birthday to: {form.birth_to.data}')
    return list(employee_info)


def employee_get_service(employee_id) -> dict:
    """
    Fetches particular employee with given id. Shows name, salary, birthday, department.

    :param employee_id: id of employee
    :return: employee(name, salary, birthday, department, id, department_id)
    """
    employee = get_employee_by_id(employee_id)
    app.logger.debug(f'Employee data: {employee}, {get_employee_department(employee.department_id)}')
    employee_info = {'name': employee.name, 'salary': employee.salary, 'birthday': employee.date_of_birth,
                     'department': get_employee_department(employee.department_id), 'id': employee.id,
                     'department_id': get_employee_department_id(employee.id)}
    return employee_info


def employee_name_service(employee_id) -> dict:
    """
    Processes the form submission. Changes the employee name in the database.
    A flash notification about the success of the operation pops up.


    :param employee_id: id of employee
    :return: employee(name, salary, birthday, department, id)
    """
    employee = get_employee_by_id(employee_id)
    app.logger.debug(f'Employee data: {employee}, {get_employee_department(employee.department_id)}')
    employee_info = {'name': employee.name, 'salary': employee.salary, 'birthday': employee.date_of_birth,
                     'department': get_employee_department(employee.department_id), 'id': employee.id}
    if request.method == 'POST':
        new_name = request.form.get('employee_new_name')
        update_employee_name(employee_info['id'], new_name)
        flash('The employee\'s name was successfully edited.', category='success')
        app.logger.debug(f'New employee name: {new_name}')
    return employee_info


def employee_salary_service(employee_id):
    """
    Processes the form submission. Changes employee salary in the database.
    A flash notification about the success of the operation pops up.

    :param employee_id: id of employee
    :return: employee(name, salary, birthday, department, id)
    """
    employee = get_employee_by_id(employee_id)
    app.logger.debug(f'Employee data: {employee}, {get_employee_department(employee.department_id)}')
    employee_info = {'name': employee.name, 'salary': employee.salary, 'birthday': employee.date_of_birth,
                     'department': get_employee_department(employee.department_id), 'id': employee.id}
    if request.method == 'POST':
        new_salary = request.form.get('employee_new_salary')
        update_employee_salary(employee_info['id'], new_salary)
        flash('The employee\'s salary was successfully edited.', category='success')
        app.logger.debug(f'New employee salary: {new_salary}')
    return employee_info


def employee_birthday_service(employee_id):
    """
    Processes the form submission. Changes employee birthday in the database.
    A flash notification about the success of the operation pops up.

    :param employee_id: id of employee
    :return: employee(name, salary, birthday, department, id)
    """
    employee = get_employee_by_id(employee_id)
    app.logger.debug(f'Employee data: {employee}, {get_employee_department(employee.department_id)}')
    employee_info = {'name': employee.name, 'salary': employee.salary, 'birthday': employee.date_of_birth,
                     'department': get_employee_department(employee.department_id), 'id': employee.id}
    if request.method == 'POST':
        new_birthday = request.form.get('employee_new_birthday')
        update_employee_birthday(employee_info['id'], new_birthday)
        flash('The employee\'s birthday was successfully edited.', category='success')
        app.logger.debug(f'New employee birthday: {new_birthday}')
    return employee_info


def employee_department_service(employee_id):
    """
    Processes the form submission. Changes employee department in the database.
    A flash notification about the success of the operation pops up.

    :param employee_id: id of employee
    :return: employee(name, salary, birthday, department, id)
    """
    employee = get_employee_by_id(employee_id)
    app.logger.debug(f'Employee data: {employee}, {get_employee_department(employee.department_id)}')
    employee_info = {'name': employee.name, 'salary': employee.salary, 'birthday': employee.date_of_birth,
                     'department': get_employee_department(employee.department_id), 'id': employee.id}
    if request.method == 'POST':
        new_department = request.form.get('employee_new_dep')
        if new_department in get_department_names():
            update_employee_department(employee_info['id'], new_department)
            flash('The employee\'s department was successfully edited.', category='success')
            app.logger.debug(f'New employee department: {new_department}')
        else:
            flash('There is no department with such name.', category='error')
            app.logger.debug(f'Invalid data: {new_department}')
    return employee_info


def employee_name_id(employee_id) -> dict:
    """
    Fetches a particular employee with given id.

    :param employee_id: id of employee
    :return: employee name and id (dict)
    """
    employee = get_employee_by_id(employee_id)
    app.logger.debug(f'Employee data: {employee}')
    employee_info = {'name': employee.name, 'id': employee.id}
    return employee_info


def remove_employee_service(employee_id):
    """
    Upon confirmation of the removal of the employee, it is deleted from the database

    :param employee_id: id of employee
    :return: redirects to 'removed_employee' page
    """
    app.logger.debug(f"{get_employee_by_id(employee_id)} is going to be removed")
    delete_employee(employee_id)
    return redirect('/employees/removed_employee')
