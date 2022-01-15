import pyautogui as pag
import logging


logg = logging.getLogger('solver.c.reader')

MOVE_DURATION = .1

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

    ###
    # EXECUTING METHODS
    ###

    def discover_field(self, field):
        logg.debug(f"discovering one field: {field}")
        pag.moveTo(field.x, field.y, duration=MOVE_DURATION)
        pag.doubleClick(field.x, field.y)

    def discover_around(self, field):
        logg.debug(f"discovering around field: {field}")
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

    def mark_multiple_mines(self, fields_to_mark):
        for field in fields_to_mark:
            self.mark_mine(field)

    def mouse_clean_pos(self):
        pag.moveTo(40, 10)
        pag.click()

    def uncover_multiple_fields(self, fields_to_uncover):
        for field in fields_to_uncover:
            self.discover_around(field)

    ###
    # READING METHODS
    ###

    def read_whole_board(self, fields):
        self.mouse_clean_pos()
        changes_flag = False
        for row in fields:
            for field in row:
                state = self._recognize_field(field)
                if field.state != state:
                    field.state = state
                    logg.debug(f'{field} state changed')
                    changes_flag = True
        logg.info(f'changes flag: {changes_flag}')
        return changes_flag

    def update_board(self, fields_to_recognize: set):
        """

        :param fields_to_recognize: set
        :return: changes_flag: bool
        """
        changes_flag = False
        fields_recognized = set()
        neighbours = set()
        for field in fields_to_recognize:
            neighbours |= field.neighbours
            logg.debug(f"added neighbours of {field} to fields_to_recognized: "
                       f"{field.neighbours}")
        fields_to_recognize |= neighbours
        while fields_to_recognize:
            logg.debug(f"Fields to reckognized: {fields_to_recognize}")
            next_fields_to_reckognized = set()
            for field in fields_to_recognize:
                current_state = field.state
                new_state = self._recognize_field(field)
                if new_state != current_state:
                    changes_flag = True
                    field.state = new_state
                    for neighbour in field.neighbours:
                        if neighbour not in fields_recognized:
                            fields_recognized.add(neighbour)
                            next_fields_to_reckognized.add(neighbour)

            fields_to_recognize = next_fields_to_reckognized
        logg.info("Recognition finished")
        logg.debug(f"Are there changes?\t\t{changes_flag}")
        return changes_flag

    def _recognize_field(self, field):
        if field.state != '*' and field.state != 'x':
            logg.debug(f"Tried to reckognize {field} but it's already known")
            return field.state

        for key in self.IMAGES:
            result = pag.locateOnScreen(
                self.IMAGES[key], region=field.region, grayscale=True,
                confidence=0.8)
            if result:
                logg.debug(f"{field} recognized as {key}")
                return key
            else:
                continue
        return 'x'




