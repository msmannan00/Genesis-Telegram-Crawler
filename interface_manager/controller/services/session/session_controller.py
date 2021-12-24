from flask import session

from interface_manager.controller.services.session.session_enums import SESSION_KEYS
from interface_manager.controller.shared.commands import SESSION_COMMANDS
from interface_manager.controller.shared.request_handler import request_handler


class session_controller(request_handler):

    __instance = None

    # Initializations
    @staticmethod
    def get_instance():
        if session_controller.__instance is None:
            session_controller()
        return session_controller.__instance

    def __init__(self):
        session_controller.__instance = self

    def __on_create_session(self, p_data):
        session[SESSION_KEYS.S_USERNAME] = p_data[0]
        session[SESSION_KEYS.S_PASSWORD] = p_data[1]
        session[SESSION_KEYS.S_ROLE] = p_data[2]

    def __exists(self):
        if session.get(SESSION_KEYS.S_USERNAME) is None or session.get(SESSION_KEYS.S_PASSWORD) is None or session.get(SESSION_KEYS.S_ROLE) is None:
            return False
        else:
            return True

    def __fetch_username(self):
        return session.get(SESSION_KEYS.S_USERNAME), session.get(SESSION_KEYS.S_ROLE)

    def invoke_trigger(self, p_command, p_data = None):
        if p_command == SESSION_COMMANDS.S_CREATE:
            self.__on_create_session(p_data)
        if p_command == SESSION_COMMANDS.S_EXISTS:
            return self.__exists()
        if p_command == SESSION_COMMANDS.S_FETCH_USER:
            return self.__fetch_username()

