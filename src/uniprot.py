#!/usr/local/bin/python3
# -*- encoding: utf-8 -*-
'''
@Brief  : Uniprot数据库爬虫
@Time   : 2023/02/12 22:10:08
@Author : https://github.com/shujuecn
'''

import requests


class UniProtAPI:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; NCE-AL10 Build/HUAWEINCE-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36"
        }
        self.fields = "accession,reviewed,id,protein_name,gene_names,organism_name,length"

    def search(self, keyword, data_format):
        if data_format not in ['xlsx', 'json']:
            raise ValueError(f"Invalid data format: {data_format}. Supported formats are 'xlsx' and 'json'.")

        url = f"https://rest.uniprot.org/uniprotkb/stream?fields={self.fields}&format={data_format}&query=%28{keyword}%29"

        response = requests.get(url)
        return response.content


uniprot = UniProtAPI()
data = uniprot.search("Muscarinic acetylcholine receptor M1", "json")
print(data)
