import enum


class TELEGRAM_COMMANDS(enum.Enum):
    S_INIT_FEEDER = 1
    S_START_FEEDER = 1
    S_GET_FEEDER = 2
    S_GET_FEEDER_SIZE = 3
    S_REMOVE_FEEDER = 4
    S_FEEDER_STATUS = 5
    S_VERIFY_LOGIN = 6
    S_FEEDER_INDEXED_DATA = 7
    S_FEEDER_EXISTS = 8

class TELEGRAM_SETTINGS:
    S_APP_ID = 13112962
    S_APP_HASH = 'db9dc29b0c62b797422f937fbc2efeab'
    S_PHONE_NUMBER = +923349798635
    S_USERNAME = "Anonymous"

class DATA_URLS:
    S_GENESIS_PATH = "https://drive.google.com/uc?export=download&id=1dGb-VMfH-Z8cMRtEs0OE0Opryiv8ihwM"
