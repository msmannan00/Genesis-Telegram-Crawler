# Local Libraries
from crawler_root.crawler.request_manager.request_handler import request_handler


# URL Queue Manager
class crawl_model(request_handler):

    # Local Queues
    __m_url_queue = {}

    # Helper Methods
    def __init__(self):
        pass

    def invoke_trigger(self, p_command, p_data=None):
        pass


