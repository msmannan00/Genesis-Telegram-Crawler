# Local Imports
from interface_manager.controller.services.elastic.elastic_enums import ELASTIC_REQUEST_COMMANDS, ELASTIC_KEYS, ELASTIC_INDEX
from interface_manager.controller.shared.request_handler import request_handler


class elastic_request_generator(request_handler):

    def __init__(self):
        pass

    def __on_search(self, p_query):
        return {ELASTIC_KEYS.S_DOCUMENT: ELASTIC_INDEX.S_MESSAGE_INDEX, ELASTIC_KEYS.S_FILTER:{'size': 100, 'query': {'bool': {'must': {'match': {'text': p_query}}}}}}

    def __on_index(self, p_json):
        m_data = [{"text": p_json.m_text, "m_username": p_json.m_username, "m_email": p_json.m_email, "m_domain_name": p_json.m_domain_name,
                   "m_channel_url": p_json.m_channel_url, "m_suspicious_keywords": p_json.m_suspicious_keywords,
                   "m_category": p_json.m_category, "m_binary_score": p_json.m_binary_score,
                   "m_urinary_score": p_json.m_urinary_score}]

        m_filtered_data = []
        for row in m_data:
            m_filtered_data.append({
                "_op_type": "index",
                "_index": ELASTIC_INDEX.S_MESSAGE_INDEX,
                "_source": row
            })
        return {ELASTIC_KEYS.S_DOCUMENT: ELASTIC_INDEX.S_MESSAGE_INDEX, ELASTIC_KEYS.S_VALUE:m_filtered_data}

    def __on_index_temp(self, p_json):
        m_data = []
        for row in p_json:
            m_data.append({
                "_op_type": "index",
                "_index": ELASTIC_INDEX.S_MESSAGE_INDEX,
                "_source": row
            })
        return {ELASTIC_KEYS.S_DOCUMENT: ELASTIC_INDEX.S_MESSAGE_INDEX, ELASTIC_KEYS.S_VALUE:m_data}

    def invoke_trigger(self, p_commands, p_data=None):
        if p_commands == ELASTIC_REQUEST_COMMANDS.M_SEARCH:
            return self.__on_search(p_data[0])
        if p_commands == ELASTIC_REQUEST_COMMANDS.M_INDEX:
            return self.__on_index(p_data[0])
        if p_commands == ELASTIC_REQUEST_COMMANDS.M_INDEX_TEMP:
            return self.__on_index_temp(p_data[0])
