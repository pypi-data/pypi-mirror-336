import logging
import pathlib
import requests
from typing_extensions import Self

PAX_SERVER_URL = 'https://pax.ulaval.ca'
LOGGER = logging.getLogger(__name__)

class Path:
    """This class behaves has a PAX replacement for the standard `pathlib.Path`.

    If {course} exists and if the specified path is relative, it adds a path prefix:
    1. `../fichiers/` if this relative folder exists locally;
    2. `/pax/shared/{course}/` else if this absolute path exists locally;
    3. or an absolute writeable `/tmp/pax/{course}/` prefix otherwise.

    Moreover, if the path does not exist, it tries to download it from the PAX server.

    Otherwise, it behaves as a standard pathlib path.
    """
    def __init__(self, *paths, course: str=None):
        # make sure course is uppercase
        course = course.upper() if course is not None else None

        if course is not None and not pathlib.Path(*paths).is_absolute():
            # check for local sibling 'fichiers' folder
            if pathlib.Path('../fichiers').is_dir():
                # use local relative file path prefix
                self._path = pathlib.Path('../fichiers', *paths)
                self._path_index = 2

            elif pathlib.Path('/pax/shared', course, *paths).exists():
                # use local absolute shared prefix
                self._path = pathlib.Path('/pax/shared', course, *paths)
                self._path_index = 4

            else:
                # use local writeable temp prefix
                self._path = pathlib.Path('/tmp/pax', course, *paths)
                self._path_index = 4

        else:
            # assume normal pathlib behavior
            self._path = pathlib.Path(*paths)
            self._path_index = 0

        # memorize course argument
        self._course = course

        if course and not self.exists():
            # try to fetch file from pax server
            self.fetch_from_pax()

    def __getattr__(self, name):
        # delegate to pathlib
        return getattr(self._path, name)

    def __str__(self) -> str:
        return str(self._path)

    def __fspath__(self):
        return str(self._path)

    def __repr__(self) -> str:
        return repr(self._path)

    def __truediv__(self, path) -> Self:
        # apply concatenation operator
        return Path(*self.parts[self._path_index:], path, course=self._course)

    def __rtruediv__(self, path) -> Self:
        # apply reverse concatenation operator
        return Path(path, *self.parts[self._path_index:], course=self._course)

    def fetch_from_pax(self) -> bool:
        # assume path cannot be fetched
        success = False

        if self._course and not self.exists():
            # set base user path (without path prefix)
            user_path = pathlib.Path(*self.parts[self._path_index:])

            # fetch file content from PAX server
            url = f'{PAX_SERVER_URL}/static/{self._course}/fichiers/{str(user_path)}'
            r = requests.get(url)
            if r.status_code == 200:
                # make sure parent path exists
                self.parent.mkdir(parents=True, exist_ok=True)

                # write downloaded content to local file
                self.write_bytes(r.content)

                # file fetched without error
                success = True

            else:
                LOGGER.warning("%d could not fetch %s", r.status_code, url)

        elif not self._course:
            LOGGER.warning("404 fetchable path must specify course id")

        return success


if __name__ == '__main__':
    assert str(Path('toto') / 'tata') == 'toto/tata'
    assert str('tata' / Path('toto')) == 'tata/toto'
    assert str(Path('toto', course='GLO-1901')) == '/tmp/pax/GLO-1901/toto'
    assert str('tata' / Path('toto', course='glo-1901')) == '/tmp/pax/GLO-1901/tata/toto'
    assert str(Path('reseau.py', course='GIF-U015')) == '/tmp/pax/GIF-U015/reseau.py'
    assert str(Path('/pax/shared', course='GLO-1901')) == '/pax/shared'
    assert Path('/toto').fetch_from_pax() is False
    assert Path('toto').fetch_from_pax() is False
    assert Path('/toto', course='glo-1901').fetch_from_pax() is False
    assert Path('toto', course='glo-1901').fetch_from_pax() is False
