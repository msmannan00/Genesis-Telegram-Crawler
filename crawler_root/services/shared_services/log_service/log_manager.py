from termcolor import colored


class log:

    __instance = None

    # Initializations
    @staticmethod
    def g():
        if log.__instance is None:
            log()
        return log.__instance

    def __init__(self):
        log.__instance = self

    # Info Logs
    def i(self, p_log):
        print(colored(p_log, 'cyan'), flush=True)

    # Info Logs
    def s(self, p_log):
        print(colored(p_log, 'green'), flush=True)

    def w(self, p_log):
        print(colored(p_log, 'yellow'), flush=True)

    # Error Logs
    def e(self, p_log):
        print(colored(p_log, 'red'), flush=True)

