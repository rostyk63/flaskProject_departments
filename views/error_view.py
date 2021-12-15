from app import app
from flask import render_template


@app.errorhandler(404)
def page_not_found(e):
    """
    Renders 'error.html' template
    :return: rendered 'error.html' template
    """
    return render_template('error.html'), 404
