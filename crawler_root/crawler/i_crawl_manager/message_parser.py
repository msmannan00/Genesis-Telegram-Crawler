# Local Imports
import re

from abc import ABC
from html.parser import HTMLParser
from crawler_root.services.helper_services.spell_check_handler import spell_checker_handler
from crawler_root.services.shared_services.topic_classifier_manager.topic_classifier import topic_classifier
from crawler_root.services.shared_services.topic_classifier_manager.topic_classifier_enums import TOPIC_CLASSFIER_COMMANDS
from crawler_root.crawler.constants.constant import PARSER
from crawler_root.crawler.helper_method.helper_method import helper_method

class message_parser(HTMLParser, ABC):

    def __init__(self):
        super().__init__()

    m_unary_tf_words = {}
    m_binary_tf_words = {}

    # --------------- Token Manager --------------- #

    def __get_score(self, p_text):
        self.m_unary_tf_words = {}
        self.m_binary_tf_words = {}

        m_unary_tf_words, m_binary_tf_words = self.__generate_score(p_text)
        return m_unary_tf_words, m_binary_tf_words

    def __update_unary_score(self, m_stemmed_word, p_length):
        if m_stemmed_word in self.m_unary_tf_words:
            m_tf_score = self.m_unary_tf_words[m_stemmed_word]
            m_tf_score = round(((m_tf_score * p_length) + 1) / p_length, 2)
            self.m_unary_tf_words[m_stemmed_word] = m_tf_score
        else:
            self.m_unary_tf_words[m_stemmed_word] = round(1 / p_length, 2)

    def __update_binary_score(self, m_stemmed_word_w1, m_stemmed_word_w2, p_length):
        if m_stemmed_word_w1 != "":
            m_binary_stemmed_word = m_stemmed_word_w1 + " " + m_stemmed_word_w2
            if m_binary_stemmed_word in self.m_binary_tf_words:
                m_tf_binary_score = self.m_binary_tf_words[m_binary_stemmed_word]
                m_tf_binary_score = round(((m_tf_binary_score * p_length) + 1) / p_length, 3)
                self.m_binary_tf_words[m_binary_stemmed_word] = m_tf_binary_score
            else:
                self.m_binary_tf_words[m_binary_stemmed_word] = round(1 / p_length, 3)
        pass

    def __generate_score(self, p_text):

        # New Line and Tab Remover
        p_text = p_text.replace('\\n', ' ')
        p_text = p_text.replace('\\t', ' ')
        p_text = p_text.replace('\\r', ' ')

        # Lower Case
        p_text = p_text.lower()

        # Remove Special Character
        p_text = re.sub('[^A-Za-z0-9]+', ' ', p_text)

        # Tokenizer
        m_word_list = p_text.split()

        # Word Checking
        m_last_word = ""
        for m_word in m_word_list:
            m_valid_status = spell_checker_handler.get_instance().validate_word(m_word)
            if m_valid_status is True:
                m_stemmed_word = spell_checker_handler.get_instance().stem_word(m_word)
                self.__update_unary_score(m_stemmed_word, len(m_word_list))
                self.__update_binary_score(m_last_word, m_stemmed_word, len(m_word_list)/4)
                m_last_word = m_word

        return "",""
    # --------------- Helper Methods --------------- #

    def extract_email(self, p_text):
        return re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", p_text)

    def extract_domain(self,p_text):
        m_domain = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+', p_text)
        m_domain_filtered = []
        for m_url in m_domain:
            m_url_cleaned = m_url
            if m_url.startswith("https") is False and m_url.startswith("http") is False:
                m_url_cleaned = "https://" + m_url
            m_host = helper_method.get_host_url(m_url_cleaned)
            if len(m_host) > 9:
                m_domain_filtered.append(m_host)
        return m_domain_filtered

    def extract_suspecious_keyword(self, p_text):
        p_text = p_text.lower()
        m_words = []
        for m_item in PARSER.S_KEYWORDS:
            if m_item in p_text:
                m_words.append(m_item)

        return m_words

    def __get_content_type(self, p_text):
        m_content_type = "general"
        if len(p_text) > 5:
            m_content_type = topic_classifier.get_instance().invoke_trigger(TOPIC_CLASSFIER_COMMANDS.S_PREDICT_CLASSIFIER, [p_text, p_text,p_text])

        return m_content_type

    # --------------- Triggers --------------- #

    def get_parsed_message(self, p_text):
        m_email = self.extract_email(p_text)
        m_domain_name = self.extract_domain(p_text)
        m_suspecious_keyword = self.extract_suspecious_keyword(p_text)
        m_content_type = self.__get_content_type(p_text)

        self.__get_score(p_text)
        return m_email, m_domain_name, self.m_unary_tf_words, self.m_binary_tf_words, m_suspecious_keyword, m_content_type

