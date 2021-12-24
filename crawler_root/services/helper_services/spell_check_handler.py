# Local Imports
import os
import sys

import nltk

from nltk import PorterStemmer
from nltk.corpus import stopwords
from crawler_root.services.helper_services.helper_method import helper_method
from crawler_root.services.shared_services.log_service.log_enums import ERROR_MESSAGES

class spell_checker_handler:
    __instance = None
    __spell_check = None
    __nltk_stopwords = None
    __m_porter_stemmer = None

    # Initializations
    @staticmethod
    def get_instance():
        if spell_checker_handler.__instance is None:
            spell_checker_handler()
        return spell_checker_handler.__instance

    def __init__(self):
        if spell_checker_handler.__instance is not None:
            raise Exception(ERROR_MESSAGES.S_SINGLETON_EXCEPTION)
        else:
            spell_checker_handler.__instance = self

            self.__spell_check = set(open(os.path.join(os.path.dirname(__file__), "dictionary")).read().split())
            self.__nltk_stopwords = stopwords.words("english")
            self.__m_porter_stemmer = PorterStemmer()

    def init_dict(self):

        self.__spell_check = set(open(os.path.join(os.path.dirname(__file__), "dictionary_small")).read().split())

    def stem_word(self, p_word):
        return self.__m_porter_stemmer.stem(p_word)

    def validate_word(self, p_word):
        if helper_method.is_stop_word(p_word) is False and p_word in self.__spell_check:
            return True
        else:
            return False

    def validate_sentence(self, p_sentence):
        sentences = nltk.sent_tokenize(p_sentence)
        for sentence in sentences:
            p_sentence = sentence.lower()
            m_valid_count = 0
            m_invalid_count = 0
            m_sentence_list = p_sentence.split()
            for word in m_sentence_list:
                if helper_method.is_stop_word(word) is True or word in self.__spell_check:
                    m_valid_count += 1
                else:
                    m_invalid_count += 1

            if m_valid_count > 0 and m_valid_count / (m_valid_count + m_invalid_count) >= 0.60:
                return " - " + sentence
        return ""
