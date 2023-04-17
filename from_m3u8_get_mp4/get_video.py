# -*- coding: utf-8 -*-
# @Author  : LouJingshuo
# @E-mail  : 3480339804@qq.com
# @Time    : 2023/4/16 15:13
# @Function: Infringement must be investigated, please indicate the source of reproduction!
"""This module is used to download the video that the user wants"""

from from_m3u8_get_mp4.decrypt_video import DecryptAES
from from_m3u8_get_mp4 import settings
import os
import shutil
import re
import asyncio
import aiohttp
import aiofiles


class GetVideoFromUrl:
    """
    This class is used to download M3U8 files from the given M3U8 file download address,
    and the downloaded M3U8 file should contain all TS video file download addresses.
    """

    proxy = ''

    def __init__(self, save_file_path, video_name, m3u8_url):
        self.save_file_path = save_file_path
        self.video_name = video_name
        self.m3u8_url = m3u8_url

    def creat_file(self):
        os.system(rf'md {self.save_file_path}\{self.video_name}\ts')
        os.system(rf'md {self.save_file_path}\{self.video_name}\decode_ts')

    async def decrypt_video(self, key):
        da = DecryptAES(save_file_path=self.save_file_path, video_name=self.video_name, key=key)
        await da.decrypt_all_ts()

    @staticmethod
    async def get_key(session, key_url):
        async with session.get(url=key_url) as resp:
            key = await resp.read()
        return key

    async def get_data(self, session, ts_url):
        """This method is used to troubleshoot various problems that can occur with connecting to the destination server"""

        headers = {
            'user-agent': settings.headers
        }

        try:
            async with session.get(url=ts_url, proxy=self.proxy, headers=headers) as resp:
                data = await resp.content.read()
                if len(data) == 0:
                    return 'no', None
                return 'yes', data
        except asyncio.exceptions.TimeoutError:
            return 'no', None
        except aiohttp.client_exceptions.ServerDisconnectedError:
            return 'no', None
        except aiohttp.client_exceptions.ClientOSError:
            return 'no', None

    async def one_ts_download(self, session, ts_url, name):
        while True:
            judge, data = await self.get_data(session, ts_url)
            if judge == 'yes':
                break
        async with aiofiles.open(rf'{self.save_file_path}\{self.video_name}\ts\{name}', 'wb') as fp:
            await fp.write(data)
        print(name + ' finished!')

    async def download_all_ts(self, session, ts_urls):
        async with aiofiles.open(rf'{self.save_file_path}\{self.video_name}\ts_name.text', 'w') as fp:
            tasks = []
            num = 0
            for ts_url in ts_urls:
                name = '{:0>5}.ts'.format(num)
                await fp.write(name + '\n')
                tasks.append(asyncio.create_task(self.one_ts_download(session, ts_url, name)))
                num += 1
            await asyncio.wait(tasks)

    @staticmethod
    async def url_compose(url_header, uncomplete_url):
        result_url_list = []
        uncomplete_url_list = uncomplete_url.split('/')
        for item in uncomplete_url_list:
            if item not in url_header:
                result_url_list.append(item)
        complete_url = url_header + '/'.join(result_url_list)
        return complete_url

    async def all_urls_get(self, session):
        async with session.get(self.m3u8_url) as resp:
            m3u8_content = await resp.read()
        async with aiofiles.open(rf'{self.save_file_path}\{self.video_name}\{self.video_name}.m3u8', 'wb') as fp:
            await fp.write(m3u8_content)

        url_header = self.m3u8_url.strip('index.m3u8')
        key_url = ''
        ts_urls = []
        async with aiofiles.open(rf'{self.save_file_path}\{self.video_name}\{self.video_name}.m3u8', 'r') as fp:
            async for item in fp:
                # extract the URL of the key
                if 'key' in item:
                    key_url = re.compile(r'URI="(?P<key_url>.*?)"', re.S).search(item).group('key_url')
                    if 'http' not in key_url:
                        key_url = await self.url_compose(url_header, key_url)

                # extract the addresses of all TS files in the file and set up a proxy
                if '#' not in item:
                    ts_url = item.strip()

                    try:
                        assert 'https' in ts_url
                        self.proxy = settings.https_proxy
                    except AssertionError:
                        self.proxy = settings.http_proxy

                    if 'http' not in ts_url:
                        ts_url = await self.url_compose(url_header, ts_url)
                    ts_urls.append(ts_url)

        return key_url, ts_urls

    async def main(self):
        # Create a folder based on the storage path provided by the user to store the corresponding video files.
        self.creat_file()
        print('The corresponding folder has been created!')

        # download the video
        timeout = aiohttp.ClientTimeout(total=30)  # Set the timeout period, which is 30 seconds by default.
        async with aiohttp.ClientSession(timeout=timeout) as session:
            key_url, ts_urls = await self.all_urls_get(session)
            await self.download_all_ts(session, ts_urls)

        # determine whether the video is encrypted
        if key_url == '':
            os.system(
                rf'copy /b {self.save_file_path}\{self.video_name}\ts\*.ts {self.save_file_path}\{self.video_name}.mp4')
        else:
            try:
                key = await self.get_key(session, key_url)
            except RuntimeError:
                async with aiohttp.ClientSession() as session1:
                    key = await self.get_key(session1, key_url)
            await self.decrypt_video(key)
            os.system(
                rf'copy /b {self.save_file_path}\{self.video_name}\decode_ts\*.ts {self.save_file_path}\{self.video_name}.mp4')
        print(self.video_name + ' finished!!')

        # clean up currently downloaded files in preparation for subsequent downloads
        shutil.rmtree(rf'{self.save_file_path}\{self.video_name}')

    def start(self):
        # encapsulates the main function for easy user calling
        asyncio.get_event_loop().run_until_complete(self.main())


class GetVideoFromFile(GetVideoFromUrl):
    """
    This class converts the user-supplied M3U8 file into an MP4 file.
    Note that this file contains all TS file (the key) download addresses in full.
    """

    def __init__(self, save_file_path, video_name, m3u8_file_path):
        super().__init__(save_file_path=save_file_path, video_name=video_name, m3u8_url=None)
        self.m3u8_file_path = m3u8_file_path

    async def all_urls_get(self, session):
        key_url = ''
        ts_urls = []
        async with aiofiles.open(rf'{self.m3u8_file_path}', 'r') as fp:
            async for item in fp:
                # extract the URL of the key
                if 'key' in item:
                    key_url = re.compile(r'URI="(?P<key_url>.*?)"', re.S).search(item).group('key_url')
                    if 'http' not in key_url:
                        key_url = await self.url_compose(url_header, key_url)

                # extract the addresses of all TS files in the file and set up a proxy
                if '#' not in item:
                    ts_url = item.strip()

                    try:
                        assert 'https' in ts_url
                        self.proxy = settings.https_proxy
                    except AssertionError:
                        self.proxy = settings.http_proxy

                    ts_urls.append(ts_url)

        return key_url, ts_urls
