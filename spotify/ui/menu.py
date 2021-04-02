import curses
import curses.panel

from .alignment import Alignment
from .panel import Panel

NEW_LINE = 10
CARRIAGE_RETURN = 13


class Menu(Panel):

    def __init__(self, title, dimensions, align=Alignment.LEFT, items=[]):
        super().__init__(title, dimensions)
        self._align = align
        self.items = items

    def get_selected(self):
        items = [x for x in self.items if x.selected]
        return None if not items else items[0]

    def _select(self, expr):
        current = self.get_selected()
        index = self.items.index(current)
        new_index = expr(index)

        # simple checks to be sure that the cursor is not out of range
        if new_index < 0:
            return

        if new_index > index and new_index >= len(self.items):
            return
        # if all OK, update cursor
        self.items[index].selected = False
        self.items[new_index].selected = True
        self._win.redrawwin()

    def next(self):
        self._select(lambda index: index + 1)

    def previous(self):
        self._select(lambda index: index - 1)

    def _initialize_items(self):
        longest_label_item = max(self.items, key=len)

        for item in self.items:
            if item != longest_label_item:
                padding = (len(longest_label_item) - len(item)) * ' '
                item.label = (f'{item}{padding}'
                if self._align == Alignment.LEFT
                else f'{padding}{item}')

            if not self.get_selected():
                self.items[0].selected = True

    def init(self):
        self._initialize_items()

    def handle_events(self, key):
        if key == curses.KEY_UP:
            self.previous()
        elif key == curses.KEY_DOWN:
            self.next()
        elif key == curses.KEY_ENTER or key == NEW_LINE or key == CARRIAGE_RETURN:
            selected_item = self.get_selected()
            return selected_item.action

    def __iter__(self):
        return iter(self.items)

    def update(self):
        pos_x = 2
        pos_y = 2
        attributes = {}
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        attributes['normal'] = curses.color_pair(1)

        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        attributes['highlighted'] = curses.color_pair(2)
        self._panel.hide()

        for item in self.items:
            if item.selected:
                attr = attributes['highlighted']
            else:
                attr = attributes['normal']
            try:
                label = f' {item.label} '
                self._win.addstr(pos_y, pos_x, label, attr)
            except:
                print(f'failed for {pos_y}, {pos_x}, {item.label}, {attr}')
            pos_y += 1
        self._panel.show()
        self._win.redrawwin()
        self._win.refresh()
