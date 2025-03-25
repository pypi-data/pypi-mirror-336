# -*- coding: UTF-8 -*-

import unittest

from poocr.api.ocr2excel import *


class TestTencent(unittest.TestCase):
    """
    测试了华为的接口，未来会从本项目中挪出去
    """

    def setUp(self):
        self.SecretId = ''
        self.SecretKey = ''

    def test_hukouben2(self):
        r = household2excel2(ak=self.SecretId, sk=self.SecretKey,
                             img_path=r'../test_files/户口本/7121976户口簿_01.png')
        r = household2excel2(ak=self.SecretId, sk=self.SecretKey,
                             img_path=r'../test_files/户口本/7220102户口薄_00.png')
        print(r)
