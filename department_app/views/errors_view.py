from app import app
from flask import render_template


@app.errorhandler(404)
def page_not_found(e):
    """
    Renders 'error404_page.html' template
    :return: rendered 'error404_page.html' template
    """
    app.logger.debug('Error 404 was handled')
    return render_template('error404_page.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    """
    Renders 'error500_page.html' template
    :return: rendered 'error500_page.html' template
    """
    app.logger.debug('Error 500 was handled')
    return render_template('error500_page.html'), 500
