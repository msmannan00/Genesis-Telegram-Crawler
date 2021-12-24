# Local Imports
import pymongo

from app import mongo
from crawler_root.services.shared_services.log_service.log_manager import log
from interface_manager.controller.constants.constant import constants
from interface_manager.controller.services.mongo.mongo_enums import MONGODB_KEYS, MONGODB_COLLECTIONS
from interface_manager.controller.services.mongo.mongo_request_generator import mongo_request_generator
from interface_manager.controller.shared.commands import MONGODB_COMMANDS
from interface_manager.controller.shared.messages import MANAGE_USER_MESSAGES
from interface_manager.controller.shared.request_handler import request_handler


class mongo_controller(request_handler):
    __instance = None
    __m_connection = None
    __m_mongo_request_generator = None

    # Initializations
    @staticmethod
    def get_instance():
        if mongo_controller.__instance is None:
            mongo_controller()
        return mongo_controller.__instance

    def __init__(self):
        mongo_controller.__instance = self
        self.__m_mongo_request_generator = mongo_request_generator()
        self.__link_connection()

    def __link_connection(self):
        self.__m_connection = mongo
        # self.__m_connection = pymongo.MongoClient('localhost', 27017)["telegram_crawler"]
        self.__initialize_database()

    def __initialize_database(self):
        try:
            m_user = self.__m_connection.create_collection(name = MONGODB_COLLECTIONS.S_USER_MODEL)
            m_user.insert(constants.S_DATABASE_DEFAULT_ENTRY)

            self.__m_connection.c_users.create_index([("m_username", pymongo.ASCENDING)],unique=True)
        except Exception:
            pass

    def __create(self, p_data):
        try:
            self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].insert_one(p_data[MONGODB_KEYS.S_FILTER])
            return True, MANAGE_USER_MESSAGES.S_INSERT_SUCCESS
        except Exception as ex:
            log.g().e("MONGO 1 : " + MANAGE_USER_MESSAGES.S_DELETE_FAILURE)
            return False, str(ex)

    def __read(self, p_data):
        try:
            documents = self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].find(p_data[MONGODB_KEYS.S_FILTER])
            return documents
        except Exception as ex:
            log.g().e("MONGO 2 : " + MANAGE_USER_MESSAGES.S_DELETE_FAILURE)
            return str(ex)

    def __update(self, p_data):
        try:
            self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].update(p_data[MONGODB_KEYS.S_FILTER], p_data[MONGODB_KEYS.S_VALUE])
            return True, MANAGE_USER_MESSAGES.S_UPDATE_SUCCESS

        except Exception as ex:
            log.g().e("MONGO 3 : " + MANAGE_USER_MESSAGES.S_DELETE_FAILURE)
            return False, str(ex)

    def __delete(self, p_data):
        try:
            documents = self.__m_connection[p_data[MONGODB_KEYS.S_DOCUMENT]].remove(p_data[MONGODB_KEYS.S_FILTER])
            return documents, MANAGE_USER_MESSAGES.S_DELETE_SUCCESS
        except Exception as ex:
            log.g().e("MONGO 4 : " + MANAGE_USER_MESSAGES.S_DELETE_FAILURE)
            return False, str(ex)

    def invoke_trigger(self, p_commands, p_data=None):
        m_request = self.__m_mongo_request_generator.invoke_trigger(p_data[0], p_data[1:])
        if p_commands == MONGODB_COMMANDS.S_CREATE:
            return self.__create(m_request)
        elif p_commands == MONGODB_COMMANDS.S_READ:
            return self.__read(m_request)
        elif p_commands == MONGODB_COMMANDS.S_UPDATE:
            return self.__update(m_request)
        elif p_commands == MONGODB_COMMANDS.S_DELETE:
            return self.__delete(m_request)
        elif p_commands == MONGODB_COMMANDS.S_INIT:
            self.__link_connection()
