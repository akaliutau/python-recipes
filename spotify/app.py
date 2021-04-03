import curses
import curses.panel
from curses import wrapper
from curses.textpad import Textbox
from curses.textpad import rectangle

from .ui import DataManager
from .ui import Menu


def show_search_screen(stdscr):
    curses.curs_set(1)
    stdscr.addstr(1, 2, "Artist name: ")

    editor_win = curses.newwin(1, 40, 3, 3)
    rectangle(stdscr, 2, 2, 4, 44)
    stdscr.refresh()

    box = Textbox(editor_win)
    box.edit()

    criteria = box.gather()
    print(f'criteria {criteria}')
    return criteria


def clear_screen(stdscr):
    stdscr.clear()
    stdscr.refresh()


def main(stdscr):
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)

    _data_manager = DataManager()

    criteria = show_search_screen(stdscr)

    height, width = stdscr.getmaxyx()
    print(f'{height}, {width}')

    albums_panel = Menu('List of albums',
                        (height, width, 0, 0))

    tracks_panel = Menu('List of tracks for the selected album',
                        (height, width, 0, 0))

    artist = _data_manager.search_artist(criteria)
    albums = _data_manager.get_artist_albums(artist['id'])

    print(f'artist record: {artist}')

    albums_panel.items = albums

    albums_panel.init()
    albums_panel.update()

    current_panel = albums_panel

    is_running = True
    print('start main cycle')
    key = 0

    while is_running:

        key = stdscr.getch()

        action = current_panel.handle_events(key)

        if action is not None:
            action_result = action()
            if current_panel == albums_panel and action_result is not None:
                # switch to track panel
                _id, uri = action_result
                tracks = _data_manager.get_album_tracklist(_id)
                current_panel.hide()
                current_panel = tracks_panel
                current_panel.items = tracks
                current_panel.init()
                current_panel.show()
            elif current_panel == tracks_panel and action_result is not None:
                _id, uri = action_result
                print(f'selected track {uri}')

                clear_screen(stdscr)
                current_panel = albums_panel
                current_panel.items = albums
                current_panel.init()
                current_panel.show()

        if key == curses.KEY_F2:
            current_panel.hide()
            criteria = show_search_screen(stdscr)
            artist = _data_manager.search_artist(criteria)
            albums = _data_manager.get_artist_albums(artist['id'])

            clear_screen(stdscr)
            current_panel = albums_panel
            current_panel.items = albums
            current_panel.init()
            current_panel.show()

        if key == 27:
            is_running = False

        current_panel.update()


try:
    wrapper(main)
except KeyboardInterrupt:
    print('Closing application')
