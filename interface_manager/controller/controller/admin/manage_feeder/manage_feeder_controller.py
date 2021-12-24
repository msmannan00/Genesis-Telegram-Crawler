# Local Imports
from interface_manager.controller.shared.messages import ERROR_MESSAGES
from interface_manager.controller.shared.request_handler import request_handler
from interface_manager.controller.controller.admin.manage_feeder.manage_feeder_model import manage_feeder_model


class manage_feeder_controller(request_handler):
    __instance = None
    __m_manage_feeder_model = None

    # Initializations
    @staticmethod
    def get_instance():
        if manage_feeder_controller.__instance is None:
            manage_feeder_controller()
        return manage_feeder_controller.__instance

    def __init__(self):
        if manage_feeder_controller.__instance is not None:
            raise Exception(ERROR_MESSAGES.S_SINGLETON_EXCEPTION)
        else:
            manage_feeder_controller.__instance = self
            self.__m_manage_feeder_model = manage_feeder_model()


    def invoke_trigger(self, p_command, p_data=None):
        return self.__m_manage_feeder_model.invoke_trigger(p_command, p_data)
