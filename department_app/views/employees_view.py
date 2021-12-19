from department_app import app
from flask import render_template, request, flash, redirect
from department_app.forms.employee_form import EmployeeForm
from department_app.service.employee_service import *
from department_app.service.department_service import get_department_names


@app.route('/employees', methods=['GET', 'POST'])
def employees():
    """
       Fetches all employees. Shows employee name, department, salary and birthday.
       Renders 'employees.html' template.
       Processes the form submission.
        Searches for employee by form parameters if at least one of them is filled in by the user.
       Redirects to 'employee_get' page in case of view of a particular employee.

       :return: rendered 'employees.html' template
       """
    form = EmployeeForm()
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
    employee_info = list(employee_info)
    app.logger.debug('employees.html was rendered')
    return render_template('employees.html', employees=employee_info, form=form)


@app.route('/employees/<int:employee_id>', methods=['GET', 'POST'])
def employee_get(employee_id):
    """
    Fetches particular employee with given id. Shows name, salary, birthday, department.
    Renders 'employee.html' template.
    Redirects to 'edit_employee_name' page in case of editing employee name.
    Redirects to 'edit_employee_salary' page in case of editing employee salary.
    Redirects to 'edit_employee_birthday' page in case of editing employee birthday.
    Redirects to 'edit_employee_department' page in case of editing employee department.
    Redirects to 'remove_employee' page in case of removing employee.
    Redirects to 'department_get' page to employee department in case of using arrow back.

    :param employee_id: id of employee
    :return: rendered 'employee.html' template
    """
    employee = get_employee_by_id(employee_id)
    app.logger.debug(f'Employee data: {employee}, {get_employee_department(employee.department_id)}')
    employee_info = {'name': employee.name, 'salary': employee.salary, 'birthday': employee.date_of_birth,
                     'department': get_employee_department(employee.department_id), 'id': employee.id,
                     'department_id': get_employee_department_id(employee.id)}
    app.logger.debug('employee.html was rendered')
    return render_template('employee.html', employee=employee_info)


@app.route('/employees/<int:employee_id>/edit_name', methods=['GET', 'POST'])
def edit_employee_name(employee_id):
    """
    Renders 'employee_edit_name.html' template.
    Processes the form submission. Changes the employee name in the database.
    A flash notification about the success of the operation pops up.
    Redirects to 'employee_get' page.

    :param employee_id: id of employee
    :return: rendered 'employee_edit_name.html' template
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
    app.logger.debug('employee_edit_name.html was rendered')
    return render_template('employee_edit_name.html', employee=employee_info)


@app.route('/employees/<int:employee_id>/edit_salary', methods=['GET', 'POST'])
def edit_employee_salary(employee_id):
    """
    Renders 'employee_edit_salary.html' template.
    Processes the form submission. Changes employee salary in the database.
    A flash notification about the success of the operation pops up.
    Redirects to 'employee_get' page.

    :param employee_id: id of employee
    :return: rendered 'employee_edit_salary.html' template
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
    app.logger.debug('employee_edit_salary.html was rendered')
    return render_template('employee_edit_salary.html', employee=employee_info)


@app.route('/employees/<int:employee_id>/edit_birthday', methods=['GET', 'POST'])
def edit_employee_birthday(employee_id):
    """
    Renders 'employee_edit_birthday.html' template.
    Processes the form submission. Changes employee birthday in the database.
    A flash notification about the success of the operation pops up.
    Redirects to 'employee_get' page.

    :param employee_id: id of employee
    :return: rendered 'employee_edit_birthday.html' template
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
    app.logger.debug('employee_edit_birthday.html was rendered')
    return render_template('employee_edit_birthday.html', employee=employee_info)


@app.route('/employees/<int:employee_id>/edit_department', methods=['GET', 'POST'])
def edit_employee_department(employee_id):
    """
    Renders 'employee_edit_department.html' template.
    Processes the form submission. Changes employee department in the database.
    A flash notification about the success of the operation pops up.
    Redirects to 'employee_get' page.

    :param employee_id: id of employee
    :return: rendered 'employee_edit_department.html' template
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
    app.logger.debug(f'employee_edit_department.html was rendered')
    return render_template('employee_edit_department.html', employee=employee_info)


@app.route('/employees/<int:employee_id>/remove', methods=['GET', 'POST'])
def remove_employee(employee_id):
    """
    Renders 'employee_remove.html' template
    Upon confirmation of the removal of the employee, it is deleted from the database,
    redirects to 'removed_employee' page.

    :param employee_id: id of employee
    :return: rendered 'employee_remove.html' template
    """
    employee = get_employee_by_id(employee_id)
    app.logger.debug(f'Employee data: {employee}')
    employee_info = {'name': employee.name, 'id': employee.id}
    if request.method == 'POST':
        app.logger.debug(f"{get_employee_by_id(employee_id)} is going to be removed")
        delete_employee(employee_id)
        return redirect('/employees/removed_employee')
    app.logger.debug(f'employee_remove.html was rendered')
    return render_template('employee_remove.html', employee=employee_info)


@app.route('/employees/removed_employee', methods=['GET'])
def removed_employee():
    """
    Renders 'removed_employee.html' template
    A flash notification about the success of the operation pops up.
    Arrow back redirects to 'employees' page

    :return: rendered 'removed_employee.html' template
    """
    app.logger.debug('Employee was removed')
    flash('The employee was successfully removed.', category='success')
    app.logger.debug(f'removed_employee.html was rendered')
    return render_template('removed_employee.html')
