# Libraries
from crawler_root.crawler.application_manager.application_enums import APPICATION_COMMANDS
from crawler_root.crawler.crawl_manager.crawl_enums import CRAWL_CONTROLLER_COMMANDS
from crawler_root.services.shared_services.log_service.log_enums import ERROR_MESSAGES
from crawler_root.crawler.request_manager.request_handler import request_handler
from crawler_root.crawler.crawl_manager.crawl_controller import crawl_controller
from crawler_root.services.shared_services.telegram_manager.telegram_controller import telegram_controller
from crawler_root.services.shared_services.telegram_manager.telegram_enums import TELEGRAM_COMMANDS


class application_controller(request_handler):
    __instance = None
    __m_crawl_controller = None

    # Initializations
    @staticmethod
    def get_instance():
        if application_controller.__instance is None:
            application_controller()
        return application_controller.__instance

    def __init__(self):
        if application_controller.__instance is not None:
            raise Exception(ERROR_MESSAGES.S_SINGLETON_EXCEPTION)
        else:
            self.__m_crawl_controller = crawl_controller()
            application_controller.__instance = self


    # External Reuqest Callbacks
    def __on_start(self):
        self.__m_crawl_controller.invoke_trigger(CRAWL_CONTROLLER_COMMANDS.S_RUN_GENERAL_CRAWLER)

    def __on_feed(self, p_data):
        self.__m_crawl_controller.invoke_trigger(CRAWL_CONTROLLER_COMMANDS.S_RUN_GENERAL_CRAWLER, p_data)

    # External Reuqest Manager
    def invoke_trigger(self, p_command, p_data=None):
        if p_command == APPICATION_COMMANDS.S_CRAWL_TELEGRAM:
            return self.__on_start()
        if p_command == APPICATION_COMMANDS.S_INSERT_FEEDER:
            return self.__on_feed(p_data)
