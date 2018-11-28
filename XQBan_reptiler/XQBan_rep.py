#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Python version: V3.7

Author: Robin&HXN

File version: V1.0

File name: XQBan_rep.py

Created on: 20181106

Resume: 

"""

import requests as rq
import pandas as pd

res_city_cate_lsit = []
res_city_cate_dirt = {}
total_res_dirt = {
    "CityName": [],
    "Category": [],
    "OrgName": [],
    "ContactTel": [],
    "LegalTel": [],
    "ContactAddr": [],
    "Tel": []
    }
city_cate_par = {
    "lat": 30.292843,
    "lng": 120.107924,
    "pageIndex": 0,
    "pageSize": 30
    }

requrl_pro = "http://my.xqban.com/admnxzcmr/provinces/pinyinlist.json"
requrl_cate = "http://my.xqban.com/admnxzcmr/catagories/lsRoot.json"

res_pro_dirt = rq.post(requrl_pro).json()
res_cate_dirt = rq.post(requrl_cate).json()


for city in res_pro_dirt["aaData"]:
    for cate in res_cate_dirt["aaData"]:
        res_city_cate_dirt = {}
        res_city_cate_dirt["city_id"] = city["id"]
        res_city_cate_dirt["city_name"] = city["name"]
        res_city_cate_dirt["cate_id"] = cate["id"]
        res_city_cate_dirt["cate_name"] = cate["name"]
        res_city_cate_lsit.append(res_city_cate_dirt)


for i in range(0, len(res_city_cate_lsit)):
    requrl_tech = "http://my.xqban.com/admnxzcmr/teacher/ls.json"
    city_cate_par["catagoriesIdes"] = int(res_city_cate_lsit[i]["cate_id"])
    city_cate_par["cityId"] = int(res_city_cate_lsit[i]["city_id"])
    res_page = rq.post(requrl_tech, params=city_cate_par).json()
    res_page_num = int(res_page["iTotalRecords"])

    if res_page_num % 30 > 0:
        page_num = (res_page_num // 30) + 1
    else:
        page_num = res_page_num // 30

    res_city_cate_lsit[i]["page_num"] = page_num
    print(res_city_cate_lsit[i])

print("step1 finish!")

for j in range(0, len(res_city_cate_lsit)):
    if res_city_cate_lsit[j]["page_num"] != 0:
        for k in range(0, int(res_city_cate_lsit[j]["page_num"])):
            requrl_tech1 = "http://my.xqban.com/admnxzcmr/teacher/ls.json"
            city_cate_par["catagoriesIdes"] = int(res_city_cate_lsit[j]["cate_id"])
            city_cate_par["cityId"] = int(res_city_cate_lsit[j]["city_id"])
            city_cate_par["pageIndex"] = int(k)
            res_total = rq.post(requrl_tech1, params=city_cate_par).json()
            for l in res_total["aaData"]:
                if l["degreeId"] == "2":
                    total_res_dirt["CityName"].append(res_city_cate_lsit[j]["city_name"])
                    total_res_dirt["Category"].append(res_city_cate_lsit[j]["cate_name"])
                    total_res_dirt["OrgName"].append(l["name"])
                    total_res_dirt["ContactTel"].append(l["contactTel"])
                    total_res_dirt["LegalTel"].append(l["legalTel"])
                    total_res_dirt["ContactAddr"].append(l["formatted_address"])
                    total_res_dirt["Tel"].append("")

    print("The %d is finished!" % j)

print("step2 finish!")

columns_list = ["城市", "分类", "机构名称", "电话", "注册电话", "联系地址", "联系电话"]
df_total = pd.DataFrame(total_res_dirt)
df_total.columns = columns_list
for index in df_total.index:
    if df_total["电话"][index] is None and df_total["注册电话"][index] is None:
        df_total.drop(index=index, inplace=True)
    elif df_total["电话"][index] is None and df_total["注册电话"][index] is not None:
        df_total["联系电话"][index] = df_total["注册电话"][index]
    elif df_total["电话"][index] is not None and df_total["注册电话"][index] is None:
        df_total["联系电话"][index] = df_total["电话"][index]
    else:
        df_total["联系电话"][index] = df_total["电话"][index] + "，" + df_total["注册电话"][index]

print("step3 finish!")

contact_tel = df_total["联系电话"]
df_total.drop(labels=["联系电话"], axis=1, inplace=True)
df_total.insert(4, "联系电话", contact_tel)
df_total.drop(labels=["电话"], axis=1, inplace=True)
df_total.drop(labels=["注册电话"], axis=1, inplace=True)
df_total.drop_duplicates(subset=["城市", "机构名称"], keep="first", inplace=True)
df_total.reset_index(drop=True)

writer = pd.ExcelWriter(u"/Users/huangxingnai/to_excel/XQBan_App_Rep_20181108.xlsx")
df_total.to_excel(writer, sheet_name="XQBan_Org_List")
writer.save()
