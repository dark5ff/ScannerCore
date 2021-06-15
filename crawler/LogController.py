import logging
import datetime

class logController:

    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s: %(levelname)s: %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            level=logging.INFO,
            filename=f'./Log/{datetime.datetime.today().strftime("%Y%m%d")}.log'
        )

        self.msg = ""

    def logInfo(self, msg):
        logging.info(msg)

