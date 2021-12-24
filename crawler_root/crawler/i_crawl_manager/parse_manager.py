# Local Imports

from crawler_root.crawler.i_crawl_manager.message_parser import message_parser


class parse_manager:
    __m_text_parser = None

    def __init__(self):
        self.__m_text_parser = message_parser()

    def on_parse_html(self, p_text):
        m_email, m_domain_name, m_urinary_score, m_binary_score, m_suspicious_keywords, m_category = self.__on_text_parser_invoke(p_text)

        return m_email, m_domain_name, m_urinary_score, m_binary_score, m_suspicious_keywords, m_category, p_text

    def __on_text_parser_invoke(self, p_text):
        return self.__m_text_parser.get_parsed_message(p_text)
