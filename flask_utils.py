from flask import session, redirect, url_for, request
from functools import wraps


def create_list_items(objects_list, naming_function, initial_string):
    for index in range(len(objects_list)):
        yield (naming_function(objects_list[index]), initial_string + str(index))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged" not in session:
            session['logged'] = False
            return redirect(url_for('login', next=request.url))
        if not session["logged"]:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function
