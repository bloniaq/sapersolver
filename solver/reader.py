import pyautogui as pag
import logging


logg = logging.getLogger('solver.c.reader')


class Reader:
    IMAGES = {
        'm': 'images/mine.png',
        '1': 'images/one.png',
        '2': 'images/two.png',
        '3': 'images/three.png',
        '4': 'images/four.png',
        '5': 'images/five.png',
        '6': 'images/six.png',
        'c': 'images/covered.png',
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
        pag.click(field.x, field.y, button='left', clicks=2)

    def discover_around(self, field):
        pag.click(field.x, field.y, button='left', clicks=2)

    def mark_bomb(self, field):
        pag.click(field.x, field.y, button='right')

    def read_whole_board(self, fields):
        self.mouse_clean_pos()
        changes_flag = False
        for row in fields:
            for field in row:
                state = self.recognize_field(field)
                if field.state != state:
                    field.state = state
                    logg.debug(f'field c{field.col} r{field.row} state: {state}')
                    changes_flag = True
        return changes_flag

    def update_board(self, fields_to_recognize):
        changes_flag = False
        fields_recognized = set()
        while fields_to_recognize:
            next_fields_to_reckognized = set()
            for field in fields_to_recognize:
                current_state = field.state
                self.mouse_clean_pos()
                new_state = self.recognize_field(field)
                if new_state != current_state:
                    changes_flag = True
                    for neighbour in field.neighbours:
                        if neighbour not in fields_recognized:
                            fields_recognized.add(neighbour)
                            next_fields_to_reckognized.add(neighbour)

            fields_to_recognize = next_fields_to_reckognized
        return changes_flag


    def recognize_field(self, field):
        if field.state != 'c' and field.state != 'x':
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
        pag.moveTo(10, 10)

    def uncover(self, fields_to_uncover):
        pass

    def gen_field(self, fields_to_reckognized):
        while True:
            yield fields_to_reckognized

