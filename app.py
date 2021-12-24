from flask import Flask, request, redirect, session
from flask_pymongo import MongoClient
from interface_manager.controller.shared.commands import MANAGE_SEARCH_COMMANDS
from settings.constant import S_SECRET_KEY, S_MONGO_URL
from settings.key import *
from settings.route import ROUTE
from interface_manager.controller.dashbaord.dashboard_controller import dashboard_controller
from interface_manager.controller.services.session.session_controller import session_controller

# Initializations

app = Flask(__name__)
app.config[S_MONGO_URI] = S_MONGO_URL
client = MongoClient(host='mongodb', port=27017,)
mongo = client["mongo_grading_system"]


# Routes
@app.route(ROUTE.S_INDEX)
def index():
    from interface_manager.controller.shared.commands import DASHBOARD_COMMANDS

    return dashboard_controller.get_instance().invoke_trigger(DASHBOARD_COMMANDS.S_DASHBOARD_TEMPLATE, None)

@app.route(ROUTE.S_MANAGE_VERIFICATION)
def manage_verification():
    from interface_manager.controller.controller.admin.manage_feeder_verification.manage_feeder_verification_controller import manage_feeder_verification_controller
    from interface_manager.controller.shared.commands import MANAGE_FEEDER_VERIFICATION_COMMANDS

    if request.args.__contains__(S_COMMAND) is not False:
        m_command = request.args.get(S_COMMAND)
    else:
        m_command = MANAGE_FEEDER_VERIFICATION_COMMANDS.S_MANAGE_VERIFICATION_TEMPLATE

    return manage_feeder_verification_controller.get_instance().invoke_trigger(m_command, None)


# Routes
@app.route(ROUTE.S_MANAGE_USER)
def manage_user():
    from interface_manager.controller.controller.admin.manage_user.manage_user_controller import manage_user_controller
    from interface_manager.controller.shared.commands import MANAGE_USER_COMMANDS

    if request.args.__contains__(S_COMMAND) is not False:
        m_command = request.args.get(S_COMMAND)
    else:
        m_command = MANAGE_USER_COMMANDS.S_MANAGE_USER_TEMPLATE

    return manage_user_controller.get_instance().invoke_trigger(m_command, None)

# Routes
@app.route(ROUTE.S_MANAGE_FEEDER)
def manage_feeder():
    from interface_manager.controller.controller.admin.manage_feeder.manage_feeder_controller import manage_feeder_controller
    from interface_manager.controller.shared.commands import MANAGE_USER_COMMANDS

    if request.args.__contains__(S_COMMAND) is not False:
        m_command = request.args.get(S_COMMAND)
    else:
        m_command = MANAGE_USER_COMMANDS.S_MANAGE_USER_TEMPLATE

    return manage_feeder_controller.get_instance().invoke_trigger(m_command, None)

@app.route(ROUTE.S_MANAGE_SEARCH)
def manage_search():
    from interface_manager.controller.controller.admin.manage_search.manage_search_controller import manage_search_controller

    if request.args.__contains__(S_COMMAND) is not False:
        m_command = request.args.get(S_COMMAND)
    else:
        m_command = MANAGE_SEARCH_COMMANDS.S_MANAGE_SEARCH_TEMPLATE

    return manage_search_controller.get_instance().invoke_trigger(m_command, None)

@app.route(ROUTE.S_LOGIN, methods=['GET', 'POST'])
def login():
    from interface_manager.controller.login.login_controller import login_controller
    from interface_manager.controller.shared.commands import SESSION_COMMANDS, LOGIN_COMMANDS

    if session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_EXISTS) is False:
        if request.args.__contains__(S_COMMAND) is not False:
            m_command = request.args.get(S_COMMAND)
        else:
            m_command = LOGIN_COMMANDS.S_LOGIN_TEMPLATE

        return login_controller.get_instance().invoke_trigger(m_command, request.args)
    else:
        return redirect(ROUTE.S_INDEX, code=302)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(ROUTE.S_INDEX)

if __name__ == '__main__':
    app.secret_key = S_SECRET_KEY
    app.config[S_SESSION_TYPE] = S_SESSION_TYPE
    app.debug = True
    app.run(host="0.0.0.0", port=5000)


'''
from settings.constant import APP_STATUS
from crawler_root.crawler.application_manager.application_controller import application_controller
from crawler_root.crawler.application_manager.application_enums import APPICATION_COMMANDS

APP_STATUS.S_CURRENT_REQUEST_PHONE_NUMBER = "+923349798635"
APP_STATUS.S_REQUEST_PHONE_NUMBER["+923349798635"] = ""
application_controller.get_instance().invoke_trigger(APPICATION_COMMANDS.S_INSERT_FEEDER,["t.me/msmannan00"])

from interface_manager.controller.services.elastic.elastic_controller import elastic_controller
from interface_manager.controller.services.elastic.elastic_enums import ELASTIC_CRUD_COMMANDS, ELASTIC_REQUEST_COMMANDS
from datetime import datetime
from datetime import datetime
doc = [{
    'author': 'zxczcx zzz',
    'text': 'zzz',
    'timestamp': datetime.now(),
},{
    'author': 'zxczcx cool',
    'text': 'cool',
    'timestamp': datetime.now(),
}]


elastic_controller.get_instance().invoke_trigger(ELASTIC_CRUD_COMMANDS.S_CREATE, [ELASTIC_REQUEST_COMMANDS.M_INDEX_TEMP, doc])
m_result = elastic_controller.get_instance().invoke_trigger(ELASTIC_CRUD_COMMANDS.S_READ, [ELASTIC_REQUEST_COMMANDS.M_SEARCH, "zzz"])
for hit in m_result['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
'''