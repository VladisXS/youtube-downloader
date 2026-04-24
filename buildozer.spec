[app]
title = YouTube Downloader
package.name = youtubedownloader
package.domain = vladis.app

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0.0
requirements = python3,kivy,yt-dlp

permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

fullscreen = 0
orientation = portrait
osx.python_version = 3.12

[buildozer]
log_level = 2
warn_on_root = 1
