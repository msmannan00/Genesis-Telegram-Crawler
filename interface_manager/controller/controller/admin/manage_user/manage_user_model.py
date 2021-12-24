import json

from flask import render_template, request, redirect

from settings.route import ROUTE
from interface_manager.controller.constants.route_template import ROUTE_TEMPLATE
from interface_manager.controller.services.mongo.mongo_controller import mongo_controller
from interface_manager.controller.services.session.session_controller import session_controller
from interface_manager.controller.shared.commands import MANAGE_USER_COMMANDS, MONGODB_COMMANDS, MONGODB_REQUEST_COMMANDS, SESSION_COMMANDS
from interface_manager.controller.shared.request_handler import request_handler
from interface_manager.controller.controller.admin.manage_user.manage_user_enums import MANAGE_USER_GET_PARAMETER_KEY, MANAGE_USER_MESSAGE_CALLBACK


class manage_user_model(request_handler):

    # Initializations
    def __init__(self):
        pass

    def __validate_parameter(self, p_command):
        m_username = request.args.get(MANAGE_USER_GET_PARAMETER_KEY.S_USERNAME)
        m_password = request.args.get(MANAGE_USER_GET_PARAMETER_KEY.S_PASSWORD)

        if p_command != MANAGE_USER_COMMANDS.S_SUBMIT_DELETE and len(m_username)<=0:
            return False, MANAGE_USER_MESSAGE_CALLBACK.S_USERNAME_EMPTY
        elif m_username == "admin":
            return False, MANAGE_USER_MESSAGE_CALLBACK.S_USERNAME_ADMIN
        elif p_command != MANAGE_USER_COMMANDS.S_SUBMIT_DELETE and len(m_password)<=0:
            return False, MANAGE_USER_MESSAGE_CALLBACK.S_PASSWORD_EMPTY
        else:
            return True, None

    def __port_data(self, p_command):
        m_username = request.args.get(MANAGE_USER_GET_PARAMETER_KEY.S_USERNAME)
        m_password = request.args.get(MANAGE_USER_GET_PARAMETER_KEY.S_PASSWORD)
        m_role = request.args.get(MANAGE_USER_GET_PARAMETER_KEY.S_ROLE)

        if p_command == MANAGE_USER_COMMANDS.S_SUBMIT_INSERT:
            m_status, m_response = mongo_controller.get_instance().invoke_trigger(MONGODB_COMMANDS.S_CREATE, [MONGODB_REQUEST_COMMANDS.S_INSERT_USER, m_username, m_password, m_role])
        elif p_command == MANAGE_USER_COMMANDS.S_SUBMIT_UPDATE:
            m_status, m_response = mongo_controller.get_instance().invoke_trigger(MONGODB_COMMANDS.S_UPDATE, [MONGODB_REQUEST_COMMANDS.S_UPDATE_USER, m_username, m_password, m_role])
        elif p_command == MANAGE_USER_COMMANDS.S_SUBMIT_DELETE:
            m_status, m_response = mongo_controller.get_instance().invoke_trigger(MONGODB_COMMANDS.S_DELETE, [MONGODB_REQUEST_COMMANDS.S_DELETE_USER, m_username])
        else:
            return redirect(ROUTE.S_INDEX, code=302)

        return m_response

    def on_manipulate_user(self, p_command):
        m_status, m_callback = self.__validate_parameter(p_command)
        if m_status is False:
            return m_callback

        return self.__port_data(p_command)

    def get_users(self):
        m_response = mongo_controller.get_instance().invoke_trigger(MONGODB_COMMANDS.S_READ, [MONGODB_REQUEST_COMMANDS.S_ALL_USER])
        m_data = []
        for m_item in m_response:
            m_data.insert(0, [m_item['m_username'], m_item['m_password'], m_item['m_role']])
        return json.dumps({'m_data':m_data})

    def __fetch_template(self):
        if session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_EXISTS) is False:
            return redirect(ROUTE.S_LOGIN, code=302)
        else:
            m_username, m_role = session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_FETCH_USER)
            return render_template(ROUTE_TEMPLATE.S_MANAGE_USER, m_data={'m_username': m_username, 'm_role': m_role})

    # External Request Handler
    def invoke_trigger(self, p_command, p_data = None):
        if p_command == MANAGE_USER_COMMANDS.S_MANAGE_USER_TEMPLATE:
          return self.__fetch_template()
        if p_command == MANAGE_USER_COMMANDS.S_SUBMIT_INSERT or p_command == MANAGE_USER_COMMANDS.S_SUBMIT_UPDATE or p_command == MANAGE_USER_COMMANDS.S_SUBMIT_DELETE:
          return self.on_manipulate_user(p_command)
        if p_command == MANAGE_USER_COMMANDS.S_SUBMIT_VIEW:
          return self.get_users()
