from flask import render_template
from department_app.forms.department_form import DepartmentForm
from department_app.views.departments_views_service import *


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
    Renders 'departments.html' template.
    Calls 'departments_service' method with additional logic.
    Redirects to 'create' page in case of creating a department.
    Redirects to 'department_get' page in case of view of a particular department.

    :return: rendered 'departments.html' template
    """
    form = DepartmentForm()
    filtered_departments = departments_service(form)
    app.logger.debug('departments.html was rendered')
    return render_template('departments.html', departments=filtered_departments, form=form)


@app.route('/departments/<int:department_id>', methods=['GET', 'POST'])
def department_get(department_id):
    """
    Renders 'department.html' template.
    Calls 'department_get_service' method with additional logic.
    Redirects to 'add_employee' page in case of adding new employee to department.
    Redirects to 'edit_department' page in case of editing department.

    :param department_id: id of department
    :return: rendered 'department.html' template
    """
    department, employees = department_get_service(department_id)
    app.logger.debug('department.html was rendered')
    return render_template('department.html', department=department,
                           employees=employees)


@app.route('/departments/<int:department_id>/add', methods=['GET', 'POST'])
def add_employee(department_id):
    """
    Renders 'employee_add.html' template.
    Calls 'add_employee_service' method with additional logic.

    :param department_id: id of department
    :return: rendered 'employee_add.html' template
    """
    department_info = add_employee_service(department_id)
    app.logger.debug('employee_add.html was rendered')
    return render_template('employee_add.html', department=department_info)


@app.route('/departments/<int:department_id>/edit', methods=['GET', 'POST'])
def edit_department(department_id):
    """
    Renders 'department_edit.html' template
    Calls 'edit_department_service' method with additional logic.
    Redirects to 'department_remove' when trying to remove department.

    :param department_id: id of department
    :return: rendered 'department_edit.html' template
    """
    department_info = edit_department_service(department_id)
    app.logger.debug('department_edit.html was rendered')
    return render_template('department_edit.html', department=department_info)


@app.route('/departments/create_department', methods=['GET', 'POST'])
def create():
    """
    Renders 'department_create.html' template
    Calls 'create_department_service' method with additional logic.

    :return: rendered 'department_create.html' template
    """
    create_department_service()
    app.logger.debug('department_create.html was rendered')
    return render_template('department_create.html')


@app.route('/departments/<int:department_id>/remove', methods=['GET', 'POST'])
def department_remove(department_id):
    """
    Renders 'department_remove.html' template.
    Calls 'department_name_id' method to get id and name of department.
    Calls 'department_remove_service' method with additional logic.
    Upon confirmation of the removal of the department, it is deleted from the database,
    redirects to 'removed_department' page.

    :param department_id: id of department
    :return: rendered 'department_remove.html' template
    """
    department_info = department_name_id(department_id)
    if request.method == 'POST':
        return department_remove_service(department_id)
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
