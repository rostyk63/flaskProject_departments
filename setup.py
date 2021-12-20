from setuptools import find_packages, setup

setup(
    name='Department App',
    version='1.0.0',
    packages=find_packages(),
    description='Web application to manage employees and departments',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'alembic==1.7.5',
        'click==8.0.3',
        'colorama==0.4.4',
        'Flask==2.0.2',
        'flask-marshmallow==0.14.0',
        'Flask-Migrate==3.1.0',
        'Flask-SQLAlchemy==2.5.1',
        'Flask-WTF==1.0.0',
        'greenlet==1.1.2',
        'gunicorn==20.1.0',
        'itsdangerous==2.0.1',
        'Jinja2==3.0.3',
        'Mako==1.1.6',
        'MarkupSafe==2.0.1',
        'marshmallow==3.14.1',
        'marshmallow-sqlalchemy==0.26.1',
        'psycopg2==2.9.2',
        'six==1.16.0',
        'SQLAlchemy==1.4.27',
        'Werkzeug==2.0.2',
        'WTForms==3.0.0'
    ],
)
