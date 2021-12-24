# Local Imports
import asyncio
import threading
import requests

from telethon import TelegramClient
from crawler_root.crawler.local_model.channel_model import channel_model
from crawler_root.services.shared_services.telegram_manager.telegram_enums import TELEGRAM_COMMANDS, TELEGRAM_SETTINGS, DATA_URLS
from crawler_root.shared_model.request_handler import request_handler


class telegram_controller(request_handler):
    __instance = None
    __m_client_list = []
    __m_user_count = 0


    # Initializations
    @staticmethod
    def get_instance():
        if telegram_controller.__instance is None:
            telegram_controller()
        return telegram_controller.__instance

    def __init__(self):
        telegram_controller.__instance = self
        self.__init_feeder()

    def __init_feeder(self):
        try:
            print("1---------------------", flush=True)
            print("1--------------------- : " + str(len(self.__m_client_list)), flush=True)
            print("1---------------------", flush=True)
            m_response = requests.get(DATA_URLS.S_GENESIS_PATH)
            for line in m_response.text.splitlines():
                m_channel_model = channel_model(line, threading.get_native_id())
                self.__m_client_list.append(m_channel_model)
        except Exception:
            pass

    async def __start_feeder(self, p_channel_url):
        for m_client_iterator in self.__m_client_list:
            if m_client_iterator.m_channel_url == p_channel_url:
                m_client = TelegramClient("anonymous_new_" + str(self.__m_user_count), TELEGRAM_SETTINGS.S_APP_ID, TELEGRAM_SETTINGS.S_APP_HASH)
                m_client_iterator.m_status = True
                m_client_iterator.m_client = m_client
                self.__m_user_count+=1

    def __get_feeder(self, p_channel_url):
        for m_client in self.__m_client_list:
            if m_client.m_channel_url == p_channel_url:
                return m_client
        return None

    def __remove_feeder(self, p_channel_url):
        for m_index in range(0, len(self.__m_client_list)):
            if self.__m_client_list[m_index].m_channel_url == p_channel_url and self.__m_client_list[m_index].m_status is True:
                self.__m_client_list[m_index].m_client.disconnect()
                self.__m_client_list[m_index].m_client = None
                self.__m_client_list[m_index].m_status = False

    def __feeder_status(self, p_channel_url):
        for m_index in range(0, len(self.__m_client_list)):
            if self.__m_client_list[m_index].m_channel_url == p_channel_url:
                return self.__m_client_list[m_index].m_status
        return False

    def __feeder_status_size(self):
        m_counter = 0
        for m_index in range(0, len(self.__m_client_list)):
            if self.__m_client_list[m_index].m_status is True:
                m_counter+=1
        return m_counter

    def __verify_login(self, p_channel_url):
        for m_index in range(0, len(self.__m_client_list)):
            if self.__m_client_list[m_index].m_channel_url == p_channel_url:
                if not self.__m_client_list[m_index].is_user_authorized():
                    return True
                else:
                    return False
        return False

    def __feeder_data(self):
        m_data = {}
        for m_client in self.__m_client_list:
            if m_client.m_status is True:
                m_data[m_client.m_channel_url] = m_client.m_channel_id

        return m_data

    def __feeder_exists(self, p_channel_url):

        for m_index in range(0, len(self.__m_client_list)):
            if self.__m_client_list[m_index].m_channel_url == p_channel_url:
                return True
        return False

    def invoke_trigger(self, p_commands, p_data=None):
        if p_commands == TELEGRAM_COMMANDS.S_INIT_FEEDER:
            self.__init_feeder()
        if p_commands == TELEGRAM_COMMANDS.S_START_FEEDER:
            asyncio.run(self.__start_feeder(p_data[0]))
        if p_commands == TELEGRAM_COMMANDS.S_GET_FEEDER:
            return self.__get_feeder(p_data[0])
        if p_commands == TELEGRAM_COMMANDS.S_REMOVE_FEEDER:
            return self.__remove_feeder(p_data[0])
        if p_commands == TELEGRAM_COMMANDS.S_FEEDER_STATUS:
            return self.__feeder_status(p_data[0])
        if p_commands == TELEGRAM_COMMANDS.S_GET_FEEDER_SIZE:
            return self.__feeder_status_size()
        if p_commands == TELEGRAM_COMMANDS.S_VERIFY_LOGIN:
            return self.__verify_login(p_data[0])
        if p_commands == TELEGRAM_COMMANDS.S_FEEDER_INDEXED_DATA:
            return self.__feeder_data()
        if p_commands == TELEGRAM_COMMANDS.S_FEEDER_EXISTS:
            return self.__feeder_exists(p_data[0])

