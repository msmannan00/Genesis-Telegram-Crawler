# Local Imports
from crawler_root.shared_model import message_model
from interface_manager.controller.services.mongo.mongo_enums import MONGODB_KEYS, MONGODB_COLLECTIONS, MONGODB_LOGIN_COLUMN
from interface_manager.controller.shared.commands import MONGODB_REQUEST_COMMANDS
from interface_manager.controller.shared.request_handler import request_handler


class mongo_request_generator(request_handler):

    def __init__(self):
        pass

    def __on_verify_credentials(self, p_username, p_password):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_USER_MODEL, MONGODB_KEYS.S_FILTER:{MONGODB_LOGIN_COLUMN.S_USERNAME: {'$eq': p_username}, MONGODB_LOGIN_COLUMN.S_PASSWORD: {'$eq': p_password}}}

    def __on_insert_user(self, p_username, p_password, p_role):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_USER_MODEL, MONGODB_KEYS.S_FILTER:{MONGODB_LOGIN_COLUMN.S_USERNAME: p_username, MONGODB_LOGIN_COLUMN.S_PASSWORD: p_password, MONGODB_LOGIN_COLUMN.S_ROLE: p_role }}

    def __on_update_user(self, p_username, p_password, p_role):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_USER_MODEL, MONGODB_KEYS.S_FILTER:{MONGODB_LOGIN_COLUMN.S_USERNAME: {'$eq': p_username}}, MONGODB_KEYS.S_VALUE:{ '$set': { MONGODB_LOGIN_COLUMN.S_PASSWORD: p_password, MONGODB_LOGIN_COLUMN.S_ROLE: p_role } }}

    def __on_delete_user(self, p_username):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_USER_MODEL, MONGODB_KEYS.S_FILTER:{MONGODB_LOGIN_COLUMN.S_USERNAME: p_username }}

    def __on_find_all_users(self):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_USER_MODEL, MONGODB_KEYS.S_FILTER:{}}

    def __user_exists(self, p_username):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_USER_MODEL, MONGODB_KEYS.S_FILTER:{MONGODB_LOGIN_COLUMN.S_USERNAME: {'$eq': p_username}}}

    def __on_save_message_model(self, p_message_model:message_model):
        return {MONGODB_KEYS.S_DOCUMENT: MONGODB_COLLECTIONS.S_MESSAGE_MODEL, MONGODB_KEYS.S_FILTER:{"m_message_text":p_message_model.m_text, "m_email":p_message_model.m_email, "m_domain_name":p_message_model.m_domain_name, "m_channel_url":p_message_model.m_channel_url, "m_suspicious_keywords":p_message_model.m_suspicious_keywords, "m_category":p_message_model.m_category, "m_binary_score":p_message_model.m_binary_score, "m_urinary_score":p_message_model.m_urinary_score}}

    def invoke_trigger(self, p_commands, p_data=None):
        if p_commands == MONGODB_REQUEST_COMMANDS.S_VERIFY_CREDENTIAL:
            return self.__on_verify_credentials(p_data[0], p_data[1])
        if p_commands == MONGODB_REQUEST_COMMANDS.S_INSERT_USER:
            return self.__on_insert_user(p_data[0], p_data[1], p_data[2])
        if p_commands == MONGODB_REQUEST_COMMANDS.S_UPDATE_USER:
            return self.__on_update_user(p_data[0], p_data[1], p_data[2])
        if p_commands == MONGODB_REQUEST_COMMANDS.S_DELETE_USER:
            return self.__on_delete_user(p_data[0])
        if p_commands == MONGODB_REQUEST_COMMANDS.S_ALL_USER:
            return self.__on_find_all_users()
        if p_commands == MONGODB_REQUEST_COMMANDS.S_SAVE_MESSAGE_MODEL:
            return self.__on_save_message_model(p_data[0])


