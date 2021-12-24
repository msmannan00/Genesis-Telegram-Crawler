from interface_manager.controller.login.login_model import login_model
from interface_manager.controller.shared.messages import ERROR_MESSAGES


class login_controller:

    # Private Variables
    __instance = None
    __m_login_model = None

    # Initializations
    @staticmethod
    def get_instance():
        if login_controller.__instance is None:
            login_controller()
        return login_controller.__instance

    def __init__(self):
        if login_controller.__instance is not None:
            raise Exception(ERROR_MESSAGES.S_SINGLETON_EXCEPTION)
        else:
            login_controller.__instance = self
            self.__m_login_model = login_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_request):
        return self.__m_login_model.invoke_trigger(p_command, p_request)
