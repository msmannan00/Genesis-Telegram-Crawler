from flask import render_template, request
from interface_manager.controller.constants.route_template import ROUTE_TEMPLATE
from interface_manager.controller.login.login_enums import LOGIN_GET_PARAMETER_KEY, LOGIN_MESSAGE_CALLBACK, MONGO_CALLBACK_KEY
from interface_manager.controller.services.mongo.mongo_controller import mongo_controller
from interface_manager.controller.services.session.session_controller import session_controller
from interface_manager.controller.shared.commands import LOGIN_COMMANDS, SESSION_COMMANDS, MONGODB_COMMANDS, MONGODB_REQUEST_COMMANDS
from interface_manager.controller.shared.messages import LOGIN_MESSAGES
from interface_manager.controller.shared.request_handler import request_handler


class login_model(request_handler):

    # Initializations
    def __init__(self):
        pass

    def __validate_parameter(self):
        m_username = request.args.get(LOGIN_GET_PARAMETER_KEY.S_USERNAME)
        m_password = request.args.get(LOGIN_GET_PARAMETER_KEY.S_PASSWORD)

        if len(m_username)<=0:
            return False, LOGIN_MESSAGE_CALLBACK.S_USERNAME_EMPTY
        elif len(m_password)<=0:
            return False, LOGIN_MESSAGE_CALLBACK.S_PASSWORD_EMPTY
        else:
            return True, None

    def __validate_data(self):
        m_username = request.args.get(LOGIN_GET_PARAMETER_KEY.S_USERNAME)
        m_password = request.args.get(LOGIN_GET_PARAMETER_KEY.S_PASSWORD)

        m_response = mongo_controller.get_instance().invoke_trigger(MONGODB_COMMANDS.S_READ, [MONGODB_REQUEST_COMMANDS.S_VERIFY_CREDENTIAL, m_username, m_password])
        m_result = next(m_response, None)
        if m_result:
            session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_CREATE, [m_username, m_password, m_result[MONGO_CALLBACK_KEY.S_ROLE]])
            return True, LOGIN_MESSAGES.S_LOGIN_SUCCESS
        else:
            return False, LOGIN_MESSAGES.S_LOGIN_FAILURE

    def __validate_login(self):
        m_status, m_message = self.__validate_parameter()
        if m_status is False:
            return m_message

        m_status, m_message = self.__validate_data()
        return m_message

    def __fetch_template(self):
        return render_template(ROUTE_TEMPLATE.S_LOGIN)

    # External Request Handler
    def invoke_trigger(self, p_command, p_data = None):
        if p_command == LOGIN_COMMANDS.S_LOGIN_TEMPLATE:
          return self.__fetch_template()
        if p_command == LOGIN_COMMANDS.S_VERIFY_LOGIN_REQUEST:
          return self.__validate_login()
