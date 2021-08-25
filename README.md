# tracemoe-py
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tracemoe-py?style=flat-square)](https://pypi.org/project/tracemoe-py/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/tracemoe-py?style=flat-square)](https://pypi.org/project/tracemoe-py/)
[![PyPI](https://img.shields.io/pypi/v/tracemoe-py?style=flat-square)](https://pypi.org/project/tracemoe-py/)
[![License](https://img.shields.io/github/license/IchBinLeoon/tracemoe-py?style=flat-square)](https://github.com/IchBinLeoon/tracemoe-py/blob/main/LICENSE)

A minimal asynchronous API wrapper for [trace.moe](https://trace.moe/).

## Installation
**Python 3.6 or higher is required.**
```shell
pip install tracemoe-py
```

## Usage
```py
import asyncio

from tracemoe import TraceMoe


async def main():
    async with TraceMoe() as tracemoe:

        # Search by image URL
        results: list = await tracemoe.search('https://XXX/XXX.jpg')
        print(results)

        # Search by image upload
        results: list = await tracemoe.search(open('/home/ichbinleoon/XXX.jpg', 'rb'))
        print(results)

        # Get account info
        info: dict = await tracemoe.me()
        print(info)

asyncio.run(main())
```

## Advanced Usage
```py
import asyncio

import aiohttp

from tracemoe import TraceMoe


async def main():

    # Use an API key
    tracemoe = TraceMoe(api_key='Your API key')

    # Cut black borders
    results: list = await tracemoe.search('https://XXX/XXX.jpg', cut_borders=True)
    print(results)

    # Filter by AniList ID
    results: list = await tracemoe.search('https://XXX/XXX.jpg', anilist_id=11617)
    print(results)

    # Include AniList info
    results: list = await tracemoe.search('https://XXX/XXX.jpg', anilist_info=True)
    print(results)
    
    await tracemoe.close()

    # Use your own aiohttp session
    session = aiohttp.ClientSession()
    tracemoe = TraceMoe(session=session)
    
    # ...
    
    await tracemoe.close()

asyncio.run(main())
```

## Contribute
Contributions are welcome! Feel free to open issues or submit pull requests!

## License
MIT © [IchBinLeoon](https://github.com/IchBinLeoon/tracemoe-py/blob/main/LICENSE)