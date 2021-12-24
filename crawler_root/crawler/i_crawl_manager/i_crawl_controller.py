# Local Imports
import asyncio
import threading
import nest_asyncio

from interface_manager.controller.services.elastic.elastic_controller import elastic_controller
from interface_manager.controller.services.elastic.elastic_enums import ELASTIC_CRUD_COMMANDS, ELASTIC_REQUEST_COMMANDS
from interface_manager.controller.services.mongo.mongo_controller import mongo_controller
from interface_manager.controller.shared.commands import MONGODB_REQUEST_COMMANDS, MONGODB_COMMANDS
from telethon import events
from crawler_root.crawler.i_crawl_manager.i_crawl_enums import ICRAWL_CONTROLLER_COMMANDS
from crawler_root.services.shared_services.log_service.log_enums import INFO_MESSAGES
from crawler_root.services.shared_services.log_service.log_manager import log
from crawler_root.crawler.request_manager.request_handler import request_handler
from crawler_root.crawler.i_crawl_manager.parse_manager import parse_manager

from crawler_root.shared_model.message_model import message_model

class i_crawl_controller(request_handler):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    nest_asyncio.apply()

    __m_message_parser = None
    __m_client = None

    def __init__(self):
        self.__m_message_parser = parse_manager()

    def __trigger_channel_parser(self, p_channel, p_channel_url):

        self.__m_client = p_channel
        @self.__m_client.on(events.NewMessage(chats=p_channel_url))
        async def newMessageListener(event):
            m_message_dict = event.message.to_dict()
            m_sender = await event.get_sender()
            m_sender_dict = m_sender.to_dict()

            m_message = m_message_dict["message"]
            m_date = m_sender_dict["date"]
            m_username = m_sender_dict["username"]

            m_email, m_domain_name, m_urinary_score, m_binary_score, m_suspicious_keywords, m_category, p_text = self.__m_message_parser.on_parse_html(m_message)
            m_message_model = message_model(p_channel_url, m_date, m_username, m_email, m_domain_name, m_urinary_score, m_binary_score, m_suspicious_keywords, m_category, p_text)
            mongo_controller.get_instance().invoke_trigger(MONGODB_COMMANDS.S_CREATE, [MONGODB_REQUEST_COMMANDS.S_SAVE_MESSAGE_MODEL, m_message_model])

            log.g().s(INFO_MESSAGES.S_SAVING_MESSAGE + " : " + str(threading.get_native_id()))

            elastic_controller.get_instance().invoke_trigger(ELASTIC_CRUD_COMMANDS.S_CREATE, [ELASTIC_REQUEST_COMMANDS.M_INDEX, m_message_model])

        with self.__m_client:
            self.__m_client.run_until_disconnected()

    def invoke_trigger(self, p_command, p_data=None):
        if p_command == ICRAWL_CONTROLLER_COMMANDS.S_START_CRAWLER_INSTANCE:
            self.__trigger_channel_parser(p_data[0], p_data[1])
