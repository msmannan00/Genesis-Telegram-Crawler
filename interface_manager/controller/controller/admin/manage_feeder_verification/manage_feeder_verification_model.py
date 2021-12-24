from flask import render_template, redirect, request
from interface_manager.controller.controller.admin.manage_feeder_verification.manage_feeder_verification_enums import MANAGE_FEEDER_VERIFICATION_GET_PARAMETER_KEY
from settings.constant import APP_STATUS
from settings.route import ROUTE
from interface_manager.controller.constants.route_template import ROUTE_TEMPLATE
from interface_manager.controller.services.session.session_controller import session_controller
from interface_manager.controller.shared.commands import SESSION_COMMANDS, MANAGE_FEEDER_VERIFICATION_COMMANDS
from interface_manager.controller.shared.request_handler import request_handler


class manage_feeder_verification_model(request_handler):

    # Initializations
    def __init__(self):
        pass

    def __validate_parameter(self, p_command):
        pass

    def __port_data(self, p_command):
       pass

    def __on_manipulate_feeder(self, p_command):
        print("FUCKS1114 : -----------------------------", flush=True)
        if p_command == MANAGE_FEEDER_VERIFICATION_COMMANDS.S_REGISTER_VERIFICATION:
            print("FUCKS1115 : -----------------------------", flush=True)
            m_feeder_verification_token = request.args.get(MANAGE_FEEDER_VERIFICATION_GET_PARAMETER_KEY.S_FEEDER_VERIFICATION_TOKEN)
            print("FUCKS1116 : ----------------------------- : " + str(m_feeder_verification_token), flush=True)
            APP_STATUS.S_REQUEST_PHONE_NUMBER[APP_STATUS.S_CURRENT_REQUEST_PHONE_NUMBER] = m_feeder_verification_token
            print("FUCKS1117 : -----------------------------1111 : " + str(APP_STATUS.S_REQUEST_PHONE_NUMBER[APP_STATUS.S_CURRENT_REQUEST_PHONE_NUMBER]), flush=True)
            return self.__on_manipulate_feeder(m_feeder_verification_token)

    def __fetch_template(self):
        print("FUCKS1113 : -----------------------------", flush=True)
        if session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_EXISTS) is False:
            return redirect(ROUTE.S_LOGIN, code=302)
        else:
            m_username, m_role = session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_FETCH_USER)
            return render_template(ROUTE_TEMPLATE.S_MANAGE_FEEDER_VERIFICATION, m_data={'username': m_username, 'm_role': m_role})

    # External Request Handler
    def invoke_trigger(self, p_command, p_data = None):
        print("FUCKS1112 : -----------------------------", flush=True)
        if p_command == MANAGE_FEEDER_VERIFICATION_COMMANDS.S_MANAGE_VERIFICATION_TEMPLATE:
            return self.__fetch_template()
        if p_command == MANAGE_FEEDER_VERIFICATION_COMMANDS.S_REGISTER_VERIFICATION:
            return self.__on_manipulate_feeder(p_command)
