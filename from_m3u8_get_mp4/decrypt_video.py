# -*- coding: utf-8 -*-
# @Author  : LouJingshuo
# @E-mail  : 3480339804@qq.com
# @Time    : 2023/4/16 15:12
# @Function: Infringement must be investigated, please indicate the source of reproduction!
"""
At present, the encryption method of M3u8 video files is generally packet connection mode (CBC).
So only the decryption algorithm of this encryption mode is written in this moudle
"""

from Crypto.Cipher import AES
import asyncio
import aiofiles


class DecryptAES:
    """This class is used to decrypt files encrypted using CBC mode in AES"""

    def __init__(self, save_file_path, video_name, key):
        self.save_file_path = save_file_path
        self.video_name = video_name
        self.key = key

    async def decrypt_one_ts(self, aes, name):
        async with aiofiles.open(rf'{self.save_file_path}\{self.video_name}\ts\{name}', 'rb') as fp1:
            data = aes.decrypt(await fp1.read())
        async with aiofiles.open(rf'{self.save_file_path}\{self.video_name}\decode_ts\{name}', 'wb') as fp2:
            await fp2.write(data)
        print(name + ' decryption complete!')

    async def decrypt_all_ts(self):
        aes = AES.new(key=self.key, IV=b'0000000000000000', mode=AES.MODE_CBC)
        async with aiofiles.open(rf'{self.save_file_path}\{self.video_name}\ts_name.text', 'r') as fp:
            tasks = []
            async for name in fp:
                name: str = name.strip('\n')
                tasks.append(asyncio.create_task(self.decrypt_one_ts(aes, name)))
            await asyncio.wait(tasks)
