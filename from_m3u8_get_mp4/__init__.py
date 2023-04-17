# -*- coding: utf-8 -*-
# @Author  : LouJingshuo
# @E-mail  : 3480339804@qq.com
# @Time    : 2023/4/16 11:01
# @Function: Infringement must be investigated, please indicate the source of reproduction!
"""
Here are some instructions for using the package named from_m3u8_get_mp4 :

* the main function of the module:

decrypt_video: This module is used to decrypt videos encrypted using CBC mode in AES.
detect_moudle: This module is used to download the relevant library and requires the user to run this file through the terminal.
settings: In this module, users can add relevant content to IP pools and UA pools to avoid anti-crawlers.
get_video: In this module, users can use different classes to achieve their goals, depending on their needs (whether the user downloads the video via URL or via a file).


* add the required libraries in the user's virtual environment
(Terminal) python detect_moudle.py (or detect the absolute path of moudle)


* the method for users to download videos using this package:

download via m3u8 url:
# from from_m3u8_get_mp4.get_video import GetVideoFromFile
# g = GetVideoFromFile(save_file_path=save_file_path, video_name=video_name, m3u8_url=m3u8_url)
# g.start()

download via m3u8 file:
# from from_m3u8_get_mp4.get_video import GetVideoFromFile
# g = GetVideoFromFile(save_file_path=save_file_path, video_name=video_name, m3u8_file_path=m3u8_file_path)
# g.start()
"""
