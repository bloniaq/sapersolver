import pyautogui as pag
import logging


logg = logging.getLogger('solver.c.reader')

MOVE_DURATION = 3

class Reader:
    IMAGES = {
        'm': 'images/mine.png',
        '1': 'images/one.png',
        '2': 'images/two.png',
        '3': 'images/three.png',
        '4': 'images/four.png',
        '5': 'images/five.png',
        '6': 'images/six.png',
        '*': 'images/covered.png',
        '_': 'images/empty.png'
    }

    def __init__(self):
        self.region = self._find_region()

    def _find_region(self):
        topleftcorner = pag.locateOnScreen('images/topleftcorner.png')
        logg.debug(f"topleftcorner results: {topleftcorner}")
        if topleftcorner is not None:
            self.left = (topleftcorner[0] + topleftcorner[2] + 5)
            self.top = topleftcorner[1] + topleftcorner[3] + 5
        return topleftcorner

    def discover_field(self, field):
        pag.moveTo(field.x, field.y, duration=MOVE_DURATION)
        pag.doubleClick(field.x, field.y)

    def discover_around(self, field):
        pag.moveTo(field.x, field.y, duration=MOVE_DURATION)
        pag.tripleClick(field.x, field.y)

    def mark_mine(self, field):
        """
        WARNING: If window hasn't focus, first click just set the focus,
        but field will be still unmarked as mine.
        :param field: Field
        :return: None
        """
        pag.moveTo(field.x, field.y, duration=MOVE_DURATION)
        pag.click(field.x, field.y, button='right')
        field.state = 'm'

    def update_fields(self, fields):
        self.mouse_clean_pos()
        changes_flag = False
        for row in fields:
            for field in row:
                state = self._recognize_field(field)
                if field.state != state:
                    field.state = state
                    logg.debug(f'field c{field.col} r{field.row} state: {state}')
                    changes_flag = True
        logg.info(f'changes flag: {changes_flag}')
        return changes_flag

    def _recognize_field(self, field):
        if field.state != '*' and field.state != 'x':
            # field.state != 'm' <--- because of unknown bug - fields are
            # marked as pm, there is try to click, but they remained unmarked
            # in reality.
            return field.state
        for key in self.IMAGES:
            result = pag.locateOnScreen(
                self.IMAGES[key], region=field.region, grayscale=True,
                confidence=0.8)
            if result:
                return key
            else:
                continue
        return 'x'

    def mouse_clean_pos(self):
        pag.moveTo(40, 10)
        pag.click()

    def uncover(self, fields_to_uncover):
        for field in fields_to_uncover:
            self.discover_around(field)

    def mark_mines(self, fields_to_mark):
        for field in fields_to_mark:
            self.mark_mine(field)
