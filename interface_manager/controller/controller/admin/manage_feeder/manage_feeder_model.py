import json

from flask import render_template, request, redirect
from crawler_root.crawler.application_manager.application_controller import application_controller
from crawler_root.crawler.application_manager.application_enums import APPICATION_COMMANDS
from crawler_root.services.shared_services.telegram_manager.telegram_controller import telegram_controller
from crawler_root.services.shared_services.telegram_manager.telegram_enums import TELEGRAM_COMMANDS
from interface_manager.controller.controller.admin.manage_feeder.manage_feeder_enums import MANAGE_FEEDER_GET_PARAMETER_KEY, MANAGE_FEEDER_MESSAGE_CALLBACK
from settings.constant import APP_STATUS
from settings.route import ROUTE
from interface_manager.controller.constants.route_template import ROUTE_TEMPLATE
from interface_manager.controller.services.session.session_controller import session_controller
from interface_manager.controller.shared.commands import MANAGE_FEEDER_COMMANDS, SESSION_COMMANDS
from interface_manager.controller.shared.request_handler import request_handler


class manage_feeder_model(request_handler):

    # Initializations
    def __init__(self):
        pass

    def __validate_parameter(self, p_command):
        m_feeder_name = request.args.get(MANAGE_FEEDER_GET_PARAMETER_KEY.S_FEEDER_NAME)
        m_feeder_phone = request.args.get(MANAGE_FEEDER_GET_PARAMETER_KEY.S_FEEDER_PHONE)

        if p_command == MANAGE_FEEDER_COMMANDS.S_SUBMIT_INSERT:

            if len(m_feeder_name)<=0:
                return False, MANAGE_FEEDER_MESSAGE_CALLBACK.S_FEEDER_EMPTY

            m_feeder_status = telegram_controller.get_instance().invoke_trigger(TELEGRAM_COMMANDS.S_FEEDER_EXISTS, [m_feeder_name])

            if  m_feeder_status is False:
                return False, MANAGE_FEEDER_MESSAGE_CALLBACK.S_FEEDER_NOT_INSTALLED
            m_status = telegram_controller.get_instance().invoke_trigger(TELEGRAM_COMMANDS.S_FEEDER_STATUS,[m_feeder_name])
            if  m_status is True:
                return False, MANAGE_FEEDER_MESSAGE_CALLBACK.S_FEEDER_ALREADY_RUNNING
            m_size = telegram_controller.get_instance().invoke_trigger(TELEGRAM_COMMANDS.S_GET_FEEDER_SIZE)
            if  m_size > 5:
                return False, MANAGE_FEEDER_MESSAGE_CALLBACK.S_MAX_FEEDER

            if len(m_feeder_phone)!=13:
                return False, MANAGE_FEEDER_MESSAGE_CALLBACK.S_PHONE_EMPTY

        elif p_command == MANAGE_FEEDER_COMMANDS.S_SUBMIT_DELETE and len(m_feeder_name) <= 0:
            return False, MANAGE_FEEDER_MESSAGE_CALLBACK.S_FEEDER_EMPTY
        return True, None

    def __port_data(self, p_command):
        if p_command == MANAGE_FEEDER_COMMANDS.S_SUBMIT_INSERT:
            m_feeder_name = request.args.get(MANAGE_FEEDER_GET_PARAMETER_KEY.S_FEEDER_NAME)
            m_feeder_phone = request.args.get(MANAGE_FEEDER_GET_PARAMETER_KEY.S_FEEDER_PHONE)

            application_controller.get_instance().invoke_trigger(APPICATION_COMMANDS.S_INSERT_FEEDER, [m_feeder_name])
            APP_STATUS.S_CURRENT_REQUEST_PHONE_NUMBER = m_feeder_phone
            APP_STATUS.S_REQUEST_PHONE_NUMBER[m_feeder_phone] = ""

            if telegram_controller.get_instance().invoke_trigger(TELEGRAM_COMMANDS.S_VERIFY_LOGIN, m_feeder_name) is True:
                return MANAGE_FEEDER_MESSAGE_CALLBACK.S_VERIFICATION_CODE_SENT
            else:
                return MANAGE_FEEDER_MESSAGE_CALLBACK.S_FEEDER_STARTED_SUCCESSFULLY
        if p_command == MANAGE_FEEDER_COMMANDS.S_SUBMIT_VIEW:

            print("----------------------",flush=True)
            print("---------------------- : " + str(json.dumps(telegram_controller.get_instance().invoke_trigger(TELEGRAM_COMMANDS.S_FEEDER_INDEXED_DATA))),flush=True)
            print("----------------------",flush=True)

            return json.dumps(telegram_controller.get_instance().invoke_trigger(TELEGRAM_COMMANDS.S_FEEDER_INDEXED_DATA))
        if p_command == MANAGE_FEEDER_COMMANDS.S_SUBMIT_DELETE:
            m_feeder_name = request.args.get(MANAGE_FEEDER_GET_PARAMETER_KEY.S_FEEDER_NAME)
            telegram_controller.get_instance().invoke_trigger(TELEGRAM_COMMANDS.S_REMOVE_FEEDER,[m_feeder_name])
            return MANAGE_FEEDER_MESSAGE_CALLBACK.S_FEEDER_REMOVED_SUCCESSFULLY

    def __on_manipulate_feeder(self, p_command):
        m_status, m_callback = self.__validate_parameter(p_command)
        if m_status is False:
            return m_callback

        return self.__port_data(p_command)

    def __fetch_template(self):
        if session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_EXISTS) is False:
            return redirect(ROUTE.S_LOGIN, code=302)
        else:
            m_username, m_role = session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_FETCH_USER)
            return render_template(ROUTE_TEMPLATE.S_MANAGE_FEEDER, m_data={'username': m_username, 'm_role': m_role})

    # External Request Handler
    def invoke_trigger(self, p_command, p_data = None):
        if p_command == MANAGE_FEEDER_COMMANDS.S_MANAGE_REGISTERATION_TEMPLATE:
            return self.__fetch_template()
        if p_command == MANAGE_FEEDER_COMMANDS.S_SUBMIT_INSERT:
            return self.__on_manipulate_feeder(p_command)
        if p_command == MANAGE_FEEDER_COMMANDS.S_SUBMIT_DELETE:
            return self.__on_manipulate_feeder(p_command)
        if p_command == MANAGE_FEEDER_COMMANDS.S_SUBMIT_VIEW:
            return self.__on_manipulate_feeder(p_command)
