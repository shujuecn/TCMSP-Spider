#!/usr/local/bin/python3
# -*- encoding: utf-8 -*-

from tcmsp import TcmspSpider


def get_data(type):

    tcmsp = TcmspSpider()
    url = f"https://tcmsp-e.com/browse.php?qc={type}"

    # 获取页面
    html = tcmsp.get_response(url)
    data = tcmsp.get_json_data(html, num=8, pattern="grid")

    # 保存数据
    tcmsp.text_to_excel(
        data,
        file_path=f"{tcmsp.sample_file_path}",
        file_name=f"{type}_data",
        index=False
    )


if __name__ == '__main__':
    type_list = ["herbs", "ingredients", "targets", "diseases"]
    for type in type_list:
        print(f"正在下载：{type}")
        get_data(type)
