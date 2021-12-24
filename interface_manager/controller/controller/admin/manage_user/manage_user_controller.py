# Local Imports
from interface_manager.controller.shared.messages import ERROR_MESSAGES
from interface_manager.controller.shared.request_handler import request_handler
from interface_manager.controller.controller.admin.manage_user.manage_user_model import manage_user_model


class manage_user_controller(request_handler):
    __instance = None
    __m_manage_user_model = None

    # Initializations
    @staticmethod
    def get_instance():
        if manage_user_controller.__instance is None:
            manage_user_controller()
        return manage_user_controller.__instance

    def __init__(self):
        if manage_user_controller.__instance is not None:
            raise Exception(ERROR_MESSAGES.S_SINGLETON_EXCEPTION)
        else:
            manage_user_controller.__instance = self
            self.__m_manage_user_model = manage_user_model()


    def invoke_trigger(self, p_command, p_data=None):
        return self.__m_manage_user_model.invoke_trigger(p_command, p_data)
