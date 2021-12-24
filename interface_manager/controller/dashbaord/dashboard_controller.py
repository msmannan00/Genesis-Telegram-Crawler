from interface_manager.controller.dashbaord.dashboard_model import dashboard_model
from interface_manager.controller.shared.messages import ERROR_MESSAGES


class dashboard_controller:

    # Private Variables
    __instance = None
    __m_dashboard_model = None

    # Initializations
    @staticmethod
    def get_instance():
        if dashboard_controller.__instance is None:
            dashboard_controller()
        return dashboard_controller.__instance

    def __init__(self):
        if dashboard_controller.__instance is not None:
            raise Exception(ERROR_MESSAGES.S_SINGLETON_EXCEPTION)
        else:
            dashboard_controller.__instance = self
            self.__m_dashboard_model = dashboard_model()

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_request):
        return self.__m_dashboard_model.invoke_trigger(p_command, p_request)
