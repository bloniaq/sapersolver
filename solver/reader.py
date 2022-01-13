import pyautogui as pag
import logging as lg

lg.basicConfig(level=lg.INFO)


class Reader:

    def __init__(self):
        self.region = self._find_region()

    def _find_region(self):
        topleftcorner = pag.locateOnScreen('images/topleftcorner.png')
        lg.info(f"topleftcorner results: {topleftcorner}")
        if topleftcorner is not None:
            self.left = (topleftcorner[0] + topleftcorner[2] + 5)
            self.top = topleftcorner[1] + topleftcorner[3] + 5
        return topleftcorner

    def discover_field(self, field):
        pag.click(field.x, field.y, button='left')

    def discover_around(self, field):
        pag.click(field.x, field.y, button='left', clicks=2)

    def mark_bomb(self, field):
        pag.click(field.x, field.y, button='right')
