# Local Imports
import threading
from crawler_root.services.shared_services.telegram_manager.telegram_controller import telegram_controller
from crawler_root.services.shared_services.telegram_manager.telegram_enums import TELEGRAM_COMMANDS
from crawler_root.crawler.crawl_manager.crawl_enums import CRAWL_CONTROLLER_COMMANDS
from crawler_root.crawler.i_crawl_manager.i_crawl_controller import i_crawl_controller
from crawler_root.crawler.i_crawl_manager.i_crawl_enums import ICRAWL_CONTROLLER_COMMANDS
from crawler_root.services.shared_services.log_service.log_enums import INFO_MESSAGES
from crawler_root.services.shared_services.log_service.log_manager import log
from crawler_root.crawler.request_manager.request_handler import request_handler
from crawler_root.crawler.crawl_manager.crawl_model import crawl_model


class crawl_controller(request_handler):

    # Local Variables
    __m_crawl_model = None

    # Crawler Instances & Threads
    __m_main_thread = None
    __m_crawler_instance_list = []

    # Initializations
    def __init__(self):
        self.__m_crawl_model = crawl_model()

    # Start Crawler Manager
    def __on_run_crawler(self):
        pass

    # ICrawler Manager
    def __init_thread_manager(self, p_feeder):
        thread_instance = threading.Thread(target=self.__create_crawler_instance, args=[p_feeder])
        thread_instance.start()

    # Awake Crawler From Sleep
    def __create_crawler_instance(self, p_channel_url):
        # try:
            telegram_controller.get_instance().invoke_trigger(TELEGRAM_COMMANDS.S_START_FEEDER, [p_channel_url])
            m_channel_model = telegram_controller.get_instance().invoke_trigger(TELEGRAM_COMMANDS.S_GET_FEEDER, [p_channel_url])
            if m_channel_model is None:
                telegram_controller.get_instance().invoke_trigger(TELEGRAM_COMMANDS.S_REMOVE_FEEDER, p_channel_url)
                return

            m_channel_crawler = m_channel_model.m_client

            # Creating Thread Instace
            m_crawler_instance = i_crawl_controller()

            # Saving Thread Instace
            log.g().i(INFO_MESSAGES.S_THREAD_CREATED + str(threading.get_native_id()))

            # Start Thread Instace
            m_crawler_instance.invoke_trigger(ICRAWL_CONTROLLER_COMMANDS.S_START_CRAWLER_INSTANCE, [m_channel_crawler, m_channel_model.m_channel_url])
            telegram_controller.get_instance().invoke_trigger(TELEGRAM_COMMANDS.S_REMOVE_FEEDER, p_channel_url)
        # except Exception as ex:
        #     log.g().e("Crawl Error : " + str(ex) )
        #     telegram_controller.get_instance().invoke_trigger(TELEGRAM_COMMANDS.S_REMOVE_FEEDER, p_channel_url)

    # Try To Get Job For Crawler Instance
    def invoke_trigger(self, p_command, p_data=None):
        if p_command == CRAWL_CONTROLLER_COMMANDS.S_RUN_GENERAL_CRAWLER:
            thread_instance = threading.Thread(target=self.__on_run_crawler, args=[])
            thread_instance.start()
        if p_command == CRAWL_CONTROLLER_COMMANDS.S_INSERT_FEEDER:
            self.__init_thread_manager(p_data[0])
