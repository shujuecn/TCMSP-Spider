# TCMSP-Spider

爬取[TCMSP数据库](https://www.tcmsp-e.com)中药物的 **Ingredients** 和 **Targets** 数据。

## 使用方法

1. 安装依赖

   ```python
   git clone https://github.com/shujuecn/TCMSP-Spider.git
   cd TCMSP-Spider
   pip3 install -r requirements.txt
   ```

2. 配置信息

   `herb_list.txt` 中填写待查询的药物名称，允许填写多个药物，允许中文、拼音或拉丁文，例如：

   ```python
   麻黄
   baizhu
   Citrus Reticulata
   ```

3. 运行程序

   ```python
   python3 spider.py
   ```

## 运行流程

1. 读取 `herb_list.txt` 文件并转为 `herb_list` ；

2. 自动获取 `token` 值；

3. 遍历 `herb_list` 中的非空元素，查询该药名对应的所有药物。因为同一中文名或拼音名，可能对应多个药物，例如：

   ```
   麻黄 -> 麻黄、麻黄根
   fuzi -> Baifuzi、Difuzi、Fuzi、Laifuzi
   ```

4. 遍历查询出的所有药物，使用正则表达式提取 **Ingredients** 和 **Targets** 数据，另存为 `.xlsx` 文件。

## 更新记录

* 2023/02/09：首次提交，已完成药名查询和药物数据下载功能。
