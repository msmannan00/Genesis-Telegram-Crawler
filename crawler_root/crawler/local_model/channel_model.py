from crawler_root.crawler.constants.strings import GENERIC_STRINGS

class channel_model:

    # Local Variables
    m_channel_url = GENERIC_STRINGS.S_EMPTY
    m_channel_id = GENERIC_STRINGS.S_EMPTY
    m_client = None
    m_status = False

    # Initializations
    def __init__(self, p_url, p_channel_id):
        self.m_channel_url = p_url
        self.m_channel_id = p_channel_id
