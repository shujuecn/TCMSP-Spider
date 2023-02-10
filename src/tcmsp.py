#!/usr/local/bin/python3
# -*- encoding: utf-8 -*-
'''
@Brief  : TCMSP数据库爬虫
@Time   : 2023/02/09 19:39:55
@Author : https://github.com/shujuecn
'''

import os
import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import lxml.html


class TcmspSpider:
    def __init__(self):

        self.root_url = "https://www.tcmsp-e.com/tcmspsearch.php"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; NCE-AL10 Build/HUAWEINCE-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
        }

        # self.file_path = "./data/"

        self.spider_file_path = "./data/spider_data/"
        self.sample_file_path = "./data/sample_data/"
        self.create_folder(self.spider_file_path)
        self.create_folder(self.sample_file_path)

        self.token = None

    def create_folder(self, path):
        """
        Create folder
        :return: None
        """

        if not os.path.exists(path):
            os.makedirs(path)

    def get_response(self, url):
        """
        Get response from url
        :param url: url
        :return: html
        """
        try:
            response = requests.get(url=url, headers=self.headers)
            response.raise_for_status()
            html = response.content.decode("utf-8")
            return html
        except requests.exceptions.RequestException as e:
            print(e)
            return

    def get_token(self):
        """
        Get token
        :return: token
        """

        html = self.get_response(self.root_url)
        root = lxml.html.fromstring(html)
        token = root.xpath('//form[@id="SearchForm"]//input[@name="token"]/@value')
        if token:
            print("token获取成功！\n")
            return token[0]
        else:
            print("token获取失败！\n")
            return

    def get_herb_name(self, herb_name):
        """
        Get herb's English name
        :param herb_name: herb's Chinese name
        :return: herb's English name
        """

        print(f"正在查询: {herb_name}...\n")

        url = f"{self.root_url}?qs=herb_all_name&q={herb_name}&token={self.token}"
        html = self.get_response(url)

        if html:
            soup = bs(html, "html.parser")
            script = soup.findAll("script")[8].__str__()
            # 解析药物的名称
            herb_three_names = re.findall(r"\n.*data:\s(.*),", script)[0]

            if herb_three_names != "[]":
                herb_three_names = json.loads(herb_three_names)
                return herb_three_names

            else:
                print(f"未查询到{herb_name}的信息！")
                return None
        else:
            pass

    def get_herb_data(self, cn_name, en_name, pinyin_name):
        """
        Get herb's data
        :param cn_name: herb's Chinese name
        :param en_name: herb's Latin name
        :param pinyin_name: herb's pinyin name
        :return: None
        """

        # Construction request link
        en_name = en_name.replace(" ", "%20")
        url = f"{self.root_url}?qr={en_name}&qsr=herb_en_name&token={self.token}"

        print(f"正在下载: {cn_name}...")
        html = self.get_response(url)
        if html:

            # 提取json数据
            # data = self.get_json_data(html)

            # 导出 Ingredients
            ingredients_pattern = "grid"
            ingredients_data = self.get_json_data(html, 11, ingredients_pattern)
            self.text_to_excel(
                ingredients_data,
                file_path=f"{self.spider_file_path}",
                file_name=f"{pinyin_name}_ingredients",
                index="MOL_ID"
            )

            # 导出 Targets
            targets_pattern = "grid2"
            targets_data = self.get_json_data(html, 11, targets_pattern)
            self.text_to_excel(
                targets_data,
                file_path=f"{self.spider_file_path}",
                file_name=f"{pinyin_name}_targets",
                index="MOL_ID"
            )

            # 导出 Disease
            # INDEX参数为False，因为Disease表格中没有MOL_ID
            disease_pattern = "grid3"
            disease_data = self.get_json_data(html, 11, disease_pattern)
            self.text_to_excel(
                disease_data,
                file_path=f"{self.spider_file_path}",
                file_name=f"{pinyin_name}_disease",
                index=False
            )

        print(f"{cn_name}下载完成！\n")

    def get_json_data(self, html, num, pattern):
        """
        Get json text
        :param html: html
        :param num: script number()
        :param pattern: regular expression
        :return: json text
        """
        soup = bs(html, "html.parser")
        scripts = soup.findAll("script")

        # The serial number of data in different pages is different
        text = scripts[num].__str__()

        pattern = rf"\$\(\"\#{pattern}\".*\n.*\n.*data\:\s(\[.*\])"
        match = re.compile(pattern).search(text)
        result = match.group(1)
        data = json.loads(result)

        return data

    def text_to_excel(self, data, file_path, file_name, index):
        """
        Regular expression extracts json data and converts to excel
        :param text: text
        :param pattern: regular expression
        :param file_name: file name
        :return: None
        """

        # Regular expression extracts json data
        if data:
            df = pd.DataFrame(data)

            # Custom index columns
            if index:
                df.set_index(index, inplace=True)
                df.to_excel(f"{file_path}{file_name}.xlsx", index=True)
            else:
                df.to_excel(f"{file_path}{file_name}.xlsx", index=False)

            print(f"已保存：{file_name}.xlsx")

        else:
            print(f"未查询到{file_name}的信息！")
