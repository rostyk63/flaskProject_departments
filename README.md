# Department App

## With this app you can:

- ### Display a list of departments and the average salary (calculated automatically) for these departments

- ### Display a list of employees in the departments with an indication of the salary for each employee and a search field to search for employees born on a certain date or in the period between dates

- ### Change (add / edit / delete) the above data

## How to build this project:

- ### Navigate to the project root folder

- ### Install the requirements:

```
pip install -r requirements.txt
python setup.py develop
```

- ### Set the following variable in config.py:

```
SECRET_KEY=<your_secret_key>

DATABASE_URL=postgres://<your_username>:<your_password>@<your_database_url>/<your_database_name>
```

- ### Run migrations to create database infrastructure:

```
python -m flask db upgrade
```

- ### (Optional) Populate the database with sample data

```
python department_app/models/populate_database.py
```

- ### Run the project locally:

```
python -m flask run
```

## Now you should be able to access the web application on the following addresses:


```
localhost:5000/

localhost:5000/departments
localhost:5000/departments/create_department
localhost:5000/departments/<int:department_id>
localhost:5000/departments/<int:department_id>/edit
localhost:5000/departments/<int:department_id>/add
localhost:5000/departments/<int:department_id>/remove
localhost:5000/departments/removed_department

localhost:5000/employees
localhost:5000/employees/<int:employee_id>
localhost:5000/employees/<int:employee_id>/edit_name
localhost:5000/employees/<int:employee_id>/edit_salary
localhost:5000/employees/<int:employee_id>/edit_birthday
localhost:5000/employees/<int:employee_id>/edit_department
localhost:5000/employees/<int:employee_id>/remove
localhost:5000/employees/removed_employee