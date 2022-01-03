# Local Imports
import os

from elasticsearch import Elasticsearch
from crawler_root.services.shared_services.log_service.log_manager import log
from interface_manager.controller.services.elastic.elastic_enums import ELASTIC_CRUD_COMMANDS, ELASTIC_KEYS
from interface_manager.controller.services.elastic.elastic_request_generator import elastic_request_generator
from interface_manager.controller.shared.messages import MANAGE_USER_MESSAGES
from interface_manager.controller.shared.request_handler import request_handler
from elasticsearch import helpers

class elastic_controller(request_handler):
    __instance = None
    __m_connection = None
    __m_elastic_request_generator = None

    # Initializations
    @staticmethod
    def get_instance():
        if elastic_controller.__instance is None:
            elastic_controller()
        return elastic_controller.__instance

    def __init__(self):
        elastic_controller.__instance = self
        self.__m_elastic_request_generator = elastic_request_generator()
        self.__link_connection()

    def __link_connection(self):
        es_host = os.environ['ELASTICSEARCH_URL']
        print('Elastic host is {}'.format(es_host))
        print("----------------------------",flush=True)
        self.__m_connection = Elasticsearch([es_host])

    def __create(self, p_data):
        try:
            helpers.bulk(self.__m_connection, p_data[ELASTIC_KEYS.S_VALUE], index=p_data[ELASTIC_KEYS.S_DOCUMENT])
        except Exception as ex:
            log.g().e("ELASTIC 1 : " + MANAGE_USER_MESSAGES.S_INSERT_FAILURE+ " : " + str(ex))
            return False, str(ex)

    def __read(self, p_data):
        try:
            m_result = self.__m_connection.search(index=p_data[ELASTIC_KEYS.S_DOCUMENT], body=p_data[ELASTIC_KEYS.S_FILTER])
            return m_result
        except Exception as ex:
            log.g().e("ELASTIC 2 : " + MANAGE_USER_MESSAGES.S_READ_FAILURE + " : " + str(ex))
            return str(ex)

    def invoke_trigger(self, p_commands, p_data=None):
        m_request = self.__m_elastic_request_generator.invoke_trigger(p_data[0], p_data[1:])
        if p_commands == ELASTIC_CRUD_COMMANDS.S_CREATE:
            return self.__create(m_request)
        elif p_commands == ELASTIC_CRUD_COMMANDS.S_READ:
            return self.__read(m_request)
