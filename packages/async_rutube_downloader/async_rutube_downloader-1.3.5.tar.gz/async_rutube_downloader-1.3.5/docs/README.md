[![release](https://img.shields.io/github/release/Reagent992/async_rutube_downloader.svg)](https://github.com/Reagent992/async_rutube_downloader/releases/latest)
[![tests](https://github.com/Reagent992/async_rutube_downloader/actions/workflows/tests.yml/badge.svg)](https://github.com/Reagent992/async_rutube_downloader/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/Reagent992/async_rutube_downloader/badge.svg?branch=main)](https://coveralls.io/github/Reagent992/async_rutube_downloader?branch=main)
[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/Reagent992/async_rutube_downloader/total?label=release%20downloads)](https://github.com/Reagent992/async_rutube_downloader/releases/latest)


English / [Russian](./README_RU.md)
# What is it?

Small project with one main function - download a video from RuTube(it's a russian copy of YouTube).

## How to use it?

### UI
- Download executable file from [Releases](https://github.com/Reagent992/async_rutube_downloader/releases/latest).

![screen_cast.gif](screen_cast.gif)

### CLI

1. Install library
```
pip install async_rutube_downloader
```
2. Run
```
rtube-cli https://rutube.ru/video/365ae8f40a2ffd2a5901ace4db799de7/
```
![cli.png](cli-en.png)

### Use in code

1. Install library
```
pip install async_rutube_downloader
```
2. Use example
```python
import asyncio
from async_rutube_downloader.downloader import Downloader

async def download():
    downloader = Downloader(
        "https://rutube.ru/video/365ae8f40a2ffd2a5901ace4db799de7/"
    )
    qualities = await downloader.fetch_video_info()
    await downloader.select_quality(max(qualities.keys()))
    await downloader.download_video()

asyncio.run(download())
```

### [Source code](./dev.md)

# About
This project was created for learning purposes and was inspired by a similar synchronous library and a book about async.

## Technical Features
- TKinter UI
- `argparse`(stdlib) CLI
- The honest progress bar shows the actual download progress.
- UI and loading work in different threads.
- UI localization.
- The async version allows you to use the full speed of your internet connection.
- [PyInstaller](https://github.com/pyinstaller/pyinstaller) is used to create an executable file.

## Dependencies

| title                                                           | description                      |
| --------------------------------------------------------------- | -------------------------------- |
| [m3u8](https://github.com/globocom/m3u8/)                       | Used for playlist parsing        |
| [aiohttp](https://github.com/aio-libs/aiohttp)                  | Async http client                |
| [aiofiles](https://github.com/Tinche/aiofiles)                  | async work with files            |
| [slugify ](https://github.com/un33k/python-slugify)             | Convert video title to file name |
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Better TKinter UI                |
