# TCMSP-Spider

爬取[TCMSP数据库](https://www.tcmsp-e.com)中的数据

## 使用方法

安装依赖

```
git clone https://github.com/shujuecn/TCMSP-Spider.git
cd TCMSP-Spider
pip3 install -r requirements.txt
```

### 根据药名查数据

在 `herb_list.txt` 中填写待查询的药物名称，允许填写多个药物，允许中文、拼音或拉丁文：

```
麻黄
Baizhu
Citrus Reticulata
```

运行程序：

```
python3 src/search_save_herbs.py
```

程序会自动获取 `token` 值，然后根据 `herb_list.txt` 中的药物名称，查询对应的所有药物。因为同一中文名或拼音名，可能对应多个药物，例如：

```
麻黄 -> 麻黄、麻黄根
fuzi -> Baifuzi、Difuzi、Fuzi、Laifuzi
```

程序根据查询结果，下载每一味药的 **Ingredients** 、 **Targets** 和 **Diseases** 数据，并以 `.xlsx` 文件格式保存在 `data/spider_data` 文件夹中。

### 下载“所有”数据

在[TCMSP Browse Database](https://tcmsp-e.com/browse.php?qc=herbs)页面，该站提供了 **All herbs**、**All ingredients**、**All targets** 和 **All diseases** 四项数据，分别包含“所有的”药名信息、药物成分信息、药物靶点信息和疾病信息。可以使用以下命令，下载这些数据，并以 `.xlsx` 文件格式保存在 `data/sample_data` 文件夹中。

```
python3 src/get_all_data.py
```

### 查询对应关系

基于“下载所有数据”，可以在药名信息、药物成分信息、药物靶点信息和疾病信息中，根据任一元素查找对应的其他元素。例如：

```
Target ID : TAR00006

Related diseases : Chronic inflammatory diseases...
Related ingredients : cyanidol...
Related herbs : 	Asteris Radix Et Rhizoma...
```

在一些特殊的情况下，这是有用的。该程序将提供此查询功能。
## 更新记录

* 2023/02/09：首次提交，已完成药名查询和药物数据下载功能。
* 2023/02/10：重构项目组成模式，完成“下载所有数据”功能。
