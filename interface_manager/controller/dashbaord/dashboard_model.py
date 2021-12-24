from flask import render_template, redirect

from settings.route import ROUTE
from interface_manager.controller.constants.route_template import ROUTE_TEMPLATE
from interface_manager.controller.services.session.session_controller import session_controller
from interface_manager.controller.shared.commands import SESSION_COMMANDS, DASHBOARD_COMMANDS
from interface_manager.controller.shared.request_handler import request_handler


class dashboard_model(request_handler):

    # Initializations
    def __init__(self):
        pass

    def __fetch_template(self):
        if session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_EXISTS) is False:
            return redirect(ROUTE.S_LOGIN, code=302)
        else:
            m_username, m_role = session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_FETCH_USER)
            return render_template(ROUTE_TEMPLATE.S_DASHBOARD, m_data = {'username':m_username, 'm_role': m_role})

    # External Request Handler
    def invoke_trigger(self, p_command, p_data = None):
        if p_command == DASHBOARD_COMMANDS.S_DASHBOARD_TEMPLATE:
            return self.__fetch_template()

