import controller
import logging

import pyautogui
pyautogui.FAILSAFE = True

# If True program skip recognition of fields at open, assuming all are covered
CLEAR_BOARD = True


logg = logging.getLogger('solver')
logg.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh = logging.FileHandler('log.log', mode='w')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s (%(funcName)s)',
    "%H:%M:%S"
)
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logg.addHandler(ch)
logg.addHandler(fh)

if __name__ == '__main__':

    app = controller.Controller(CLEAR_BOARD)
