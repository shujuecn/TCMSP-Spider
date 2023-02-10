#!/usr/local/bin/python3
# -*- encoding: utf-8 -*-

from tcmsp import TcmspSpider


def get_herb_data():
    """
    Search for herbs to be queried and download data.
    :return: None
    """
    tcmsp = TcmspSpider()

    # 构建药物列表
    herb_list = []
    with open("./herb_list.txt", "r", encoding="utf-8") as f:
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
    get_herb_data()
