# paxutils
Miscellaneous utilities for PAX notebooks.

The `path.Path` class is a dropin replacement for `pathlib.Path` in the context of the PAX platform. Use the standard `pathlib` in any other context.

# Usage
```python
from paxutils.path import Path

# define path for file `myfile` in the context of the PAX course `GIF-U014`
path = Path('myfile', course='GIF-U014')
...
```

# build distribution
python -m build

# upload to pypi
twine upload dist/*
