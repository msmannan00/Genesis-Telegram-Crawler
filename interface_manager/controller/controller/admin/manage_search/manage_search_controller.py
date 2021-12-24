# Local Imports
from interface_manager.controller.shared.messages import ERROR_MESSAGES
from interface_manager.controller.shared.request_handler import request_handler
from interface_manager.controller.controller.admin.manage_search.manage_search_model import manage_search_model


class manage_search_controller(request_handler):
    __instance = None
    __m_manage_course_model = None

    # Initializations
    @staticmethod
    def get_instance():
        if manage_search_controller.__instance is None:
            manage_search_controller()
        return manage_search_controller.__instance

    def __init__(self):
        if manage_search_controller.__instance is not None:
            raise Exception(ERROR_MESSAGES.S_SINGLETON_EXCEPTION)
        else:
            manage_search_controller.__instance = self
            self.__m_manage_course_model = manage_search_model()


    def invoke_trigger(self, p_command, p_data=None):
        return self.__m_manage_course_model.invoke_trigger(p_command, p_data)
