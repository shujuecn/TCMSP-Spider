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


class TCMSP:
    def __init__(self):

        self.root_url = "https://www.tcmsp-e.com/tcmspsearch.php"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; NCE-AL10 Build/HUAWEINCE-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
        }

        self.file_path = "./output/"
        self.create_folder()

        self.token = None

    def create_folder(self):
        """
        Create folder
        :return: None
        """

        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)

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
        :param en_name: herb's English name
        :return: None
        """

        # Construction request link
        en_name = en_name.replace(" ", "%20")
        url = f"{self.root_url}?qr={en_name}&qsr=herb_en_name&token={self.token}"

        print(f"正在下载: {cn_name}...")
        html = self.get_response(url)
        if html:
            soup = bs(html, "html.parser")
            scripts = soup.findAll("script")
            text = scripts[11].__str__()

            # 导出 Ingredients
            ingredients_pattern = r"\$\(\"\#grid\".*\n.*\n.*data\:\s(\[.*\])"
            self.text_to_excel(text, ingredients_pattern, f"{pinyin_name}_ingredients")

            # 导出 Targets
            targets_pattern = r"\$\(\"\#grid2\".*\n.*\n.*data\:\s(\[.*\])"
            self.text_to_excel(text, targets_pattern, f"{pinyin_name}_targets")
        print()

    def text_to_excel(self, text, pattern, file_name):
        """
        Regular expression extracts json data and converts to excel
        :param text: text
        :param pattern: regular expression
        :param file_name: file name
        :return: None
        """

        # Regular expression extracts json data
        match = re.compile(pattern).search(text)
        result = match.group(1)
        data = json.loads(result)

        if data:
            df = pd.DataFrame(data)
            df.set_index("MOL_ID", inplace=True)
            df.to_excel(f"{self.file_path}{file_name}.xlsx", index=True)
            print(f"已保存：{file_name}.xlsx")
        else:
            print("未查询到数据！")


def main():
    """
    Main function
    """
    tcmsp = TCMSP()

    # 构建药物列表
    herb_list = []
    with open("herb_list.txt", "r", encoding="utf-8") as f:
        for line in f:
            herb_list.append(line.strip())

    print(f"共有{len(herb_list)}个药物需要查询！\n")

    tcmsp.token = tcmsp.get_token()

    # 遍历需要查询的药物
    for herb in herb_list:
        if herb == "":
            continue

        herb_three_names = tcmsp.get_herb_name(herb)

        # 如果查询到多个药物，逐一下载
        for name in herb_three_names:
            herb_cn_name = name["herb_cn_name"]
            herb_en_name = name["herb_en_name"]
            herb_pinyin_name = name["herb_pinyin"]
            tcmsp.get_herb_data(herb_cn_name, herb_en_name, herb_pinyin_name)


if __name__ == "__main__":
    main()
