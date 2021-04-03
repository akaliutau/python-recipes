from .menu_item import MenuItem

from spotify.jukebox.core import search_artist
from spotify.jukebox.core import get_artist_albums
from spotify.jukebox.core import get_album_tracks

from .empty_results_error import EmptyResultsError

from spotify.jukebox.auth import authenticate
from spotify.jukebox.core import read_config


def _format_artist_label(item):
    print(f'item: {item}')
    return f'{item["name"]} ({item["type"]}, release date: {item["release_date"]})'


def _format_track_label(item):
    time = int(item['duration_ms'])
    minutes = int((time / 60000) % 60)
    seconds = int((time / 1000) % 60)

    track_name = item['name']

    return f'{track_name} - [{minutes}:{seconds}]'


class DataManager():

    def __init__(self):
        self._conf = read_config()
        self._auth = authenticate(self._conf)

    def search_artist(self, criteria):
        print(f'searching for {criteria}')
        results = search_artist(criteria, self._auth)
        items = results['artists']['items']
        print(f'items: {0}', items[0])

        if not items:
            raise EmptyResultsError(f'Could not find the artist: {criteria}')

        return items[0]

    def get_artist_albums(self, artist_id, max_items=20):

        albums = get_artist_albums(artist_id, self._auth)['items']

        if not bool(albums):
            raise EmptyResultsError(('Could not find any albums for'
                                     f'the artist_id: {artist_id}'))

        return [MenuItem(_format_artist_label(album), album)
                for album in albums[:max_items]]

    def get_album_tracklist(self, album_id):

        results = get_album_tracks(album_id, self._auth)

        if not results:
            raise EmptyResultsError('Could not find the tracks for this album')

        tracks = results['items']

        return [MenuItem(_format_track_label(track), track)
                for track in tracks]

