from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
from typing import Optional

from yutipy.deezer import Deezer
from yutipy.exceptions import InvalidValueException
from yutipy.itunes import Itunes
from yutipy.kkbox import KKBox
from yutipy.models import MusicInfo, MusicInfos
from yutipy.musicyt import MusicYT
from yutipy.spotify import Spotify
from yutipy.utils.cheap_utils import is_valid_string


class YutipyMusic:
    """A class that can be used to retrieve music information from all music platforms available in ``yutipy``.

    This is useful when you want to get music information (especially streaming link) from all available platforms.
    Instead of calling each service separately, you can use this class to get the information from all services at once.
    """

    def __init__(self) -> None:
        """Initializes the YutipyMusic class."""
        self.music_info = MusicInfos()
        self.album_art_priority = ["deezer", "kkbox", "spotify", "musicyt", "itunes"]

    def search(self, artist: str, song: str) -> Optional[MusicInfos]:
        """
        Searches for a song by artist and title.

        Parameters
        ----------
        artist : str
            The name of the artist.
        song : str
            The title of the song.

        Returns
        -------
        Optional[MusicInfos_]
            The music information if found, otherwise None.
        """
        if not is_valid_string(artist) or not is_valid_string(song):
            raise InvalidValueException(
                "Artist and song names must be valid strings and can't be empty."
            )

        services = [
            (Deezer, "deezer"),
            (Itunes, "itunes"),
            (KKBox, "kkbox"),
            (MusicYT, "musicyt"),
            (Spotify, "spotify"),
        ]

        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(service().search, artist, song): name
                for service, name in services
            }

            for future in as_completed(futures):
                service_name = futures[future]
                result = future.result()
                self._combine_results(result, service_name)

        if len(self.music_info.url) == 0:
            return None

        return self.music_info

    def _combine_results(self, result: Optional[MusicInfo], service_name: str) -> None:
        """
        Combines the results from different services.

        Parameters
        ----------
        result : Optional[MusicInfo]
            The music information from a service.
        service_name : str
            The name of the streaming service.
        """
        if not result:
            return

        attributes = [
            "album_title",
            "album_type",
            "artists",
            "genre",
            "isrc",
            "lyrics",
            "release_date",
            "tempo",
            "title",
            "type",
            "upc",
        ]

        for attr in attributes:
            if getattr(result, attr) and (
                not getattr(self.music_info, attr) or service_name == "spotify"
            ):
                setattr(self.music_info, attr, getattr(result, attr))

        if result.album_art:
            current_priority = self.album_art_priority.index(service_name)
            existing_priority = (
                self.album_art_priority.index(self.music_info.album_art_source)
                if self.music_info.album_art_source
                else len(self.album_art_priority)
            )
            if current_priority < existing_priority:
                self.music_info.album_art = result.album_art
                self.music_info.album_art_source = service_name

        self.music_info.id[service_name] = result.id
        self.music_info.url[service_name] = result.url


if __name__ == "__main__":
    yutipy_music = YutipyMusic()
    artist_name = input("Artist Name: ")
    song_name = input("Song Name: ")
    pprint(yutipy_music.search(artist_name, song_name))
