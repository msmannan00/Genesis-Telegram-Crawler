from crawler_root.crawler.constants.strings import GENERIC_STRINGS

class message_model:

    # Local Variables
    m_channel_url = GENERIC_STRINGS.S_EMPTY
    m_date = GENERIC_STRINGS.S_EMPTY
    m_username = GENERIC_STRINGS.S_EMPTY
    m_email = []
    m_domain_name = []
    m_urinary_score = []
    m_binary_score = []
    m_suspicious_keywords = []
    m_category = GENERIC_STRINGS.S_EMPTY
    m_text = GENERIC_STRINGS.S_EMPTY

    # Initializations
    def __init__(self, p_channel_url, p_date, p_username,p_email, p_domain_name, p_urinary_score, p_binary_score, p_suspicious_keywords, p_category, p_text):
        self.m_channel_url = p_channel_url
        self.m_date = p_date
        self.m_username = p_username
        self.m_email = p_email
        self.m_domain_name = p_domain_name
        self.m_urinary_score = p_urinary_score
        self.m_binary_score = p_binary_score
        self.m_suspicious_keywords = p_suspicious_keywords
        self.m_category = p_category
        self.m_text = p_text
