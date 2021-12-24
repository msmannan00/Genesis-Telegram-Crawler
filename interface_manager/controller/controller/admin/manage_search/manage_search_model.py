import json

from flask import render_template, redirect, request

from crawler_root.services.shared_services.topic_classifier_manager.topic_classifier import topic_classifier
from crawler_root.services.shared_services.topic_classifier_manager.topic_classifier_enums import \
    TOPIC_CLASSFIER_COMMANDS
from interface_manager.controller.controller.admin.manage_search.manage_search_enums import \
    MANAGE_SEARCH_GET_PARAMETER_KEY
from interface_manager.controller.services.elastic.elastic_controller import elastic_controller
from interface_manager.controller.services.elastic.elastic_enums import ELASTIC_REQUEST_COMMANDS, ELASTIC_CRUD_COMMANDS
from settings.route import ROUTE
from interface_manager.controller.constants.route_template import ROUTE_TEMPLATE
from interface_manager.controller.services.session.session_controller import session_controller
from interface_manager.controller.shared.commands import SESSION_COMMANDS, MANAGE_SEARCH_COMMANDS
from interface_manager.controller.shared.request_handler import request_handler


class manage_search_model(request_handler):

    # Initializations
    def __init__(self):
        pass

    def __validate_parameter(self, p_command):
        m_query = request.args.get(MANAGE_SEARCH_GET_PARAMETER_KEY.S_QUERY)

    def __port_data(self, p_command):
       pass

    def __on_manipulate_search(self, p_command):

        m_query = None
        if MANAGE_SEARCH_GET_PARAMETER_KEY.S_QUERY not in request.args:
            m_query = ""
        else:
            m_query = request.args.get(MANAGE_SEARCH_GET_PARAMETER_KEY.S_QUERY)

        from datetime import datetime
        doc = [{"text": "how are you i am fine", "m_email": "msmannan00", "m_domain_name": ["bbc.com","cnn.com"],
                   "m_channel_url": "id-1123@hidden", "m_suspicious_keywords": ["sex","porn"],
                   "m_category": "adult", "m_binary_score": [],
                   "m_urinary_score": []}, {"text": "i am really fucked up", "m_email": "cloudysaqib", "m_domain_name": ["umt.com","comsats.com"],
                   "m_channel_url": "id-5523@hidden", "m_suspicious_keywords": ["piss","shower"],
                   "m_category": "general", "m_binary_score": [],
                   "m_urinary_score": []}]

        elastic_controller.get_instance().invoke_trigger(ELASTIC_CRUD_COMMANDS.S_CREATE, [ELASTIC_REQUEST_COMMANDS.M_INDEX_TEMP, doc])
        m_result = elastic_controller.get_instance().invoke_trigger(ELASTIC_CRUD_COMMANDS.S_READ, [ELASTIC_REQUEST_COMMANDS.M_SEARCH, m_query])


        m_result_final = m_result['hits']['hits']

        return str(m_result_final)

    def __fetch_template(self):
        if session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_EXISTS) is False:
            return redirect(ROUTE.S_LOGIN, code=302)
        else:
            m_username, m_role = session_controller.get_instance().invoke_trigger(SESSION_COMMANDS.S_FETCH_USER)
            return render_template(ROUTE_TEMPLATE.S_MANAGE_SEARCH, m_data={'username': m_username, 'm_role': m_role})

    # External Request Handler
    def invoke_trigger(self, p_command, p_data = None):
        if p_command == MANAGE_SEARCH_COMMANDS.S_MANAGE_SEARCH_TEMPLATE:
            return self.__fetch_template()
        if p_command == MANAGE_SEARCH_COMMANDS.S_MANAGE_SEARCH:
            return self.__on_manipulate_search(p_command)
