#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Python version: V3.7

Author: Robin&HXN

File version: V1.0

File name: TEXue_rep.py

Created on: 20181109

Resume: 

"""

import requests as rq
import pandas as pd

res_cate_list_fa = []

par = {
    "lat": 30.292843,
    "lng": 120.107924,
    "pageNum": 1,
    "pageSize": 10
    }

total_res_dirt = {
    "Category":[],
    "OrgName":[],
    "ContactTel":[],
    "ContactAddr":[],
    }

requrl_cate = u"https://newapi.taoerxue.cn/1/education/typeParentList"
res_cate_dirt = rq.get(requrl_cate).json()

for data1 in res_cate_dirt["data"]:
    res_cate_dirt_fa = {}
    res_cate_dirt_fa["cate_id"] = data1["id"]
    res_cate_dirt_fa["cate_name"] = data1["name"]
    res_cate_list_fa.append(res_cate_dirt_fa)

print("step1: Category is download!")

for index in range(0, len(res_cate_list_fa)):
    print(index)
    par["typeId"] = res_cate_list_fa[index]["cate_id"]
    for page_num in range(1,1000):
        par["pageNum"] = page_num
        requrl_ser = u"https://newapi.taoerxue.cn/1/search/getSearchEducationList"
        res_dirt = rq.post(requrl_ser, params=par).json()
        if len(res_dirt) >= 3:
            for org1 in res_dirt["data"]:
                total_res_dirt["Category"].append(res_cate_list_fa[index]["cate_name"])
                total_res_dirt["OrgName"].append(org1["name"])
                total_res_dirt["ContactTel"].append(org1["telephone"])
                total_res_dirt["ContactAddr"].append(org1["detailedAddress"])
        else:
            break

    print(index)




columns_list = ["分类", "机构名称", "联系电话", "联系地址"]
df_total = pd.DataFrame(total_res_dirt)
df_total.columns = columns_list
df_total.index += 1
writer = pd.ExcelWriter(u"/Users/huangxingnai/to_excel/TEXue_App_Rep_20181109.xlsx")
df_total.to_excel(writer, sheet_name="TEXue_Org_List")
writer.save()





