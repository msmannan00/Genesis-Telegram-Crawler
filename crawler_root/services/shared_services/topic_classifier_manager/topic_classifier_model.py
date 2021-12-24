import os
import pickle
import warnings
import pandas as pd

from crawler_root.services.constants.constant import SHARED_CONSTANT, CLASSIFIER_PATH_CONSTANT
from crawler_root.services.shared_services.topic_classifier_manager.topic_classifier_enums import TOPIC_CLASSFIER_MODEL
from crawler_root.shared_model.request_handler import request_handler

warnings.filterwarnings("ignore", category=RuntimeWarning)
class topic_classifier_model(request_handler):

    def __init__(self):
        self.__m_vectorizer = None
        self.__m_feature_selector = None
        self.__m_classifier = None
        self.__m_classifier_trained = False

    def __classifier_exists(self):
        if self.__m_classifier_trained is not True:
                self.__m_classifier_trained = True
                self.__load_classifier()
                return True
        else:
            return True

    def __load_classifier(self):
        self.__m_vectorizer = pickle.load(open((os.path.join(os.path.dirname(__file__), CLASSIFIER_PATH_CONSTANT.S_VECTORIZER_PATH)), 'rb'))
        self.__m_feature_selector = pickle.load(open((os.path.join(os.path.dirname(__file__), CLASSIFIER_PATH_CONSTANT.S_SELECTKBEST_PATH)), 'rb'))
        self.__m_classifier = pickle.load(open((os.path.join(os.path.dirname(__file__), CLASSIFIER_PATH_CONSTANT.S_CLASSIFIER_PICKLE_PATH)), 'rb'))

    def __predict_classifier(self, p_title, p_description, p_keyword):
                m_status = self.__classifier_exists()
        #if m_status is True:
            #try:
                m_title = pd.Series([p_title])
                m_description = pd.Series([p_description])
                m_keyword = pd.Series([p_keyword])

                if m_title is None:
                    m_title = ""
                if m_description is None:
                    m_description = ""
                if m_keyword is None:
                    m_keyword = []

                m_title_vectorizer_data = self.__m_vectorizer.transform(m_title.values.astype('U'))
                m_description_vectorizer_data = self.__m_vectorizer.transform(m_description.astype('U'))
                m_keyword_vectorizer_data = self.__m_vectorizer.transform(m_keyword.astype('U'))

                m_title_vectorized = pd.DataFrame(m_title_vectorizer_data.toarray(),
                                                  columns=self.__m_vectorizer.get_feature_names())
                m_description_vectorized = pd.DataFrame(m_description_vectorizer_data.toarray(),
                                                        columns=self.__m_vectorizer.get_feature_names())
                m_keyword_vectorized = pd.DataFrame(m_keyword_vectorizer_data.toarray(),
                                                    columns=self.__m_vectorizer.get_feature_names())

                m_dataframe = m_title_vectorized + m_description_vectorized + m_keyword_vectorized

                X = self.__m_feature_selector.transform(m_dataframe)

                m_predictions = list(self.__m_classifier.predict_proba(X)[0])
                max_value = max(m_predictions)
                max_index = m_predictions.index(max_value)

                if max_value > 0.70:
                    m_predictions = self.__m_classifier.classes_[max_index]
                else:
                    m_predictions = "General"

                return m_predictions
            #except Exception:
            #    return "UN_KNOWN"
        #else:
        #    return "UN_KNOWN"

    def invoke_trigger(self, p_command, p_data=None):
        if p_command == TOPIC_CLASSFIER_MODEL.S_PREDICT_CLASSIFIER:
            return self.__predict_classifier(p_data[0], p_data[1], p_data[2])
