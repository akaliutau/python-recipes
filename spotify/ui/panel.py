import curses
import curses.panel
from uuid import uuid1


class Panel:

    def __init__(self, title, dimensions):
        height, width, y, x = dimensions

        print(f'creating new window w={width} h={height} @ ({x},{y})')
        print(height, width, y, x)
        self._win = curses.initscr()
        self._win.clear()
        self._win.box()
        self._win.refresh()
        self._panel = curses.panel.new_panel(self._win)
        self._panel.show()

        self.title = title
        self._id = uuid1()

        self._set_title()


    def hide(self):
        self._panel.hide()

    def _set_title(self):
        formatted_title = f' {self.title} '
        self._win.addstr(0, 2, formatted_title, curses.A_REVERSE)

    def show(self):
        self._win.clear()
        self._win.box()
        self._set_title()
        curses.curs_set(1)
        self._panel.show()

    def is_visible(self):
        return not self._panel.hidden()

    def __eq__(self, other):
        return self._id == other._id

