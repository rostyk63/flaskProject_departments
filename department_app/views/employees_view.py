from flask import render_template
from department_app.forms.employee_form import EmployeeForm
from department_app.views.employees_views_service import *


@app.route('/employees', methods=['GET', 'POST'])
def employees():
    """
    Renders 'employees.html' template.
    Calls 'employees_service' method with additional logic.
    Redirects to 'employee_get' page in case of view of a particular employee.

    :return: rendered 'employees.html' template
    """
    form = EmployeeForm()
    filtered_employees = employees_service(form)
    app.logger.debug('employees.html was rendered')
    return render_template('employees.html', employees=filtered_employees, form=form)


@app.route('/employees/<int:employee_id>', methods=['GET', 'POST'])
def employee_get(employee_id):
    """
    Renders 'employee.html' template.
    Calls 'employee_get_service' method with additional logic.
    Redirects to 'edit_employee_name' page in case of editing employee name.
    Redirects to 'edit_employee_salary' page in case of editing employee salary.
    Redirects to 'edit_employee_birthday' page in case of editing employee birthday.
    Redirects to 'edit_employee_department' page in case of editing employee department.
    Redirects to 'remove_employee' page in case of removing employee.
    Redirects to 'department_get' page to employee department in case of using arrow back.

    :param employee_id: id of employee
    :return: rendered 'employee.html' template
    """
    employee_info = employee_get_service(employee_id)
    app.logger.debug('employee.html was rendered')
    return render_template('employee.html', employee=employee_info)


@app.route('/employees/<int:employee_id>/edit_name', methods=['GET', 'POST'])
def edit_employee_name(employee_id):
    """
    Renders 'employee_edit_name.html' template.
    Calls 'employee_name_service' method with additional logic.
    Redirects to 'employee_get' page.

    :param employee_id: id of employee
    :return: rendered 'employee_edit_name.html' template
    """
    employee_info = employee_name_service(employee_id)
    app.logger.debug('employee_edit_name.html was rendered')
    return render_template('employee_edit_name.html', employee=employee_info)


@app.route('/employees/<int:employee_id>/edit_salary', methods=['GET', 'POST'])
def edit_employee_salary(employee_id):
    """
    Renders 'employee_edit_salary.html' template.
    Calls 'employee_salary_service' method with additional logic.
    Redirects to 'employee_get' page.

    :param employee_id: id of employee
    :return: rendered 'employee_edit_salary.html' template
    """
    employee_info = employee_salary_service(employee_id)
    app.logger.debug('employee_edit_salary.html was rendered')
    return render_template('employee_edit_salary.html', employee=employee_info)


@app.route('/employees/<int:employee_id>/edit_birthday', methods=['GET', 'POST'])
def edit_employee_birthday(employee_id):
    """
    Renders 'employee_edit_birthday.html' template.
    Calls 'employee_birthday_service' method with additional logic.
    Redirects to 'employee_get' page.

    :param employee_id: id of employee
    :return: rendered 'employee_edit_birthday.html' template
    """
    employee_info = employee_birthday_service(employee_id)
    app.logger.debug('employee_edit_birthday.html was rendered')
    return render_template('employee_edit_birthday.html', employee=employee_info)


@app.route('/employees/<int:employee_id>/edit_department', methods=['GET', 'POST'])
def edit_employee_department(employee_id):
    """
    Renders 'employee_edit_department.html' template.
    Calls 'employee_department_service' method with additional logic.
    Redirects to 'employee_get' page.

    :param employee_id: id of employee
    :return: rendered 'employee_edit_department.html' template
    """
    employee_info = employee_department_service(employee_id)
    app.logger.debug(f'employee_edit_department.html was rendered')
    return render_template('employee_edit_department.html', employee=employee_info)


@app.route('/employees/<int:employee_id>/remove', methods=['GET', 'POST'])
def remove_employee(employee_id):
    """
    Renders 'employee_remove.html' template
    Calls 'employee_name_id' method to get id and name of department.
    Calls 'remove_employee_service' method with additional logic.
    Upon confirmation of the removal of the employee, it is deleted from the database,
    redirects to 'removed_employee' page.

    :param employee_id: id of employee
    :return: rendered 'employee_remove.html' template
    """
    employee_info = employee_name_id(employee_id)
    if request.method == 'POST':
        return remove_employee_service(employee_id)
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
