import pyautogui as pag
import logging


logg = logging.getLogger('solver.c.reader')


class Reader:

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

    def update_fields(self, fields):
        for row in fields:
            for field in row:
                state = self._recognize_field(field)

    def _recognize_field(self, field):
        pass
