> ⚠️ **归档说明 / Archived**
>
> 本项目（`TCMSP-Spider`）已停止维护并进入归档状态（**不再更新、不再适配 TCMSP 新版页面/接口变化**）。
>
> ✅ 请迁移至新项目：**TCMSP-Exporter**（浏览器内运行的 Tampermonkey 油猴脚本，替代旧版 Python 爬虫导出方案）  
> 新仓库地址：https://github.com/shujuecn/TCMSP-Exporter
>
> ---
>
> This repository is **archived** and **no longer maintained**.  
> Please use the replacement project: **TCMSP-Exporter**  
> https://github.com/shujuecn/TCMSP-Exporter

# TCMSP-Spider

TCMSP-Spider is a Python tool for extracting data from [TCMSP](https://www.tcmsp-e.com) (Traditional Chinese Medicine Systems Pharmacology Database and Analysis Platform) website. It allows you to search for a specific drug and retrieve its related ingredients, targets, and diseases. Additionally, you can download "all" data of drugs, ingredients, targets, and diseases. The tool can be easily configured to query and download a list of drugs, eliminating the need to manually pass `token` parameters.

## Installation

1. Clone the repository and navigate to the project directory:

```
git clone https://github.com/shujuecn/TCMSP-Spider.git
cd TCMSP-Spider
```

2. Install the required dependencies:

```
pip3 install -r requirements.txt
```

## Usage
### Searching data by drug name

1. Add the names of the drugs you want to search for in `herb_list.txt`. You can add multiple drugs, and the names can be written in Chinese, Pinyin or Latin, for example:

```
麻黄
Baizhu
Citrus Reticulata
```

2. Run the following command to start the search process:

```
python3 src/search_save_herbs.py
```

The program will automatically obtain the `token` value and query all the drugs specified in `herb_list.txt`. Because a single Chinese or Pinyin name may correspond to multiple drugs, the program will download the ingredients, targets, and diseases of each drug, and save them in an Excel (.xlsx) file in the `data/spider_data` folder.

```
麻黄 -> 麻黄、麻黄根
fuzi -> Baifuzi、Difuzi、Fuzi、Laifuzi
```
### Downloading "all" data

On the [TCMSP Browse Database](https://tcmsp-e.com/browse.php?qc=herbs) page, the website provides four types of data, including "all" drugs, ingredients, targets, and diseases. You can use the following command to download these data and save them in an Excel (.xlsx) file in the `data/sample_data` folder.

```
python3 src/get_all_data.py
```

### Querying relationships

Using the data downloaded with "Get all data," you can use the program to query the relationships between drugs, ingredients, targets, and diseases. For example:

```
Target ID: TAR00006

Related diseases: Chronic inflammatory diseases...
Related ingredients: cyanidol...
Related herbs: Asteris Radix Et Rhizoma...
```

While it is not currently available in the current version of the program, in the future, it may be possible to use the data downloaded using "Get all data" to query for relationships between different elements, such as finding all the ingredients related to a certain disease or target. This feature is not yet implemented in the current version, but may be added in a future update.

## LICENSE

This project is released under the MIT open source license. If you have any suggestions or feedback, please feel free to submit an issue or pull request.

## Changelog

* 2023/02/09: Initial commit. Completed the search function and data download function.
* 2023/02/10: Refactored the project structure and added the "download all data" function.

