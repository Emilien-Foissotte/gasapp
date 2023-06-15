import re
import uuid

from dash.dependencies import Input, Output, State

from app import application, db, User

@application.callback(
    Output("userlogged", "data"),
    Input("selected_user", "value")
)
def log_user(username):
    loguser = User.query.filter_by(name=username).first()
    if not loguser is None:
        data = {
            "username": loguser.name,
            "id": loguser.id
        }
        return data
    else:
        return None


@application.callback(
    Output("selected_user", "options"),
    Input("interval_updateusers", "n_intervals")
)
def update_userlist(n):
    if n:
        users_list =[user.name for user in User.query.all()]
        ret_list = [
            {"label": user,
             "value": user} for user in users_list]
        return ret_list

@application.callback(
    [
        Output("collapse_message_useradd", "is_open"),
        Output("collapse_message_useradd", "children"),
        Output("submit-useradd", "disabled")
    ],
    Input("useradd_input", "value")
    )
def callback_disable_submituser(value):
        if value == "":
            return False, "", True
        elif re.search(r'[^a-zA-Z0-9\\s]+', value):
            return True, "Caractère invalide", True
        elif value in [user.name for user in User.query.all()]:
            return True, f"Utilisateur {value} déjà enregistré", True
        else:
            return False, "", False

@application.callback(
    Output("useradd_input", "value"),
    State("useradd_input", "value"),
    Input("submit-useradd", "n_clicks"),
    )
def add_user(username, submit):
    if submit:
        newuser = User()
        newuser.name = username
        newuser.id = uuid.uuid4().hex
        db.session.add(newuser)
        db.session.commit()
    return ""
