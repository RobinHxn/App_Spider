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

par2 = {
    "eId": 0,
    "pageNum": 1,
    "pageSize": 10
    }

total_res_dirt = {
    "Category": [],
    "OrgId": [],
    "OrgName": [],
    "ContactTel": [],
    "ContactAddr": [],
    "LessonNum": [],
    "Star": [],
    "OryUrl": []
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
    par["typeId"] = res_cate_list_fa[index]["cate_id"]
    for page_num in range(1, 1000):
        par["pageNum"] = page_num
        requrl_ser = u"https://newapi.taoerxue.cn/1/search/getSearchEducationList"
        res_dirt = rq.post(requrl_ser, params=par).json()
        if len(res_dirt) >= 3:
            for org1 in res_dirt["data"]:
                total_res_dirt["Category"].append(res_cate_list_fa[index]["cate_name"])
                total_res_dirt["OrgId"].append(org1["id"])
                total_res_dirt["OrgName"].append(org1["name"])
                total_res_dirt["ContactTel"].append(org1["telephone"])
                total_res_dirt["ContactAddr"].append(org1["detailedAddress"])
        else:
            break

    for id in total_res_dirt["OrgId"]:
        par2["eId"] = int(id)
        lesson_num = 0
        for page_num2 in range(1,1000):
            par2["pageNum"] = page_num2
            requrl_course = u"https://newapi.taoerxue.cn/1/course/getRecommendCourseList"
            res_dirt1 = rq.post(requrl_course, params=par2).json()
            if len(res_dirt1) >= 3:
                lesson_num += len(res_dirt1["data"])
            else:
                break

        total_res_dirt["LessonNum"].append(int(lesson_num))

        requrl_orgdt = u"https://newapi.taoerxue.cn/1/education/getDetailInfo?id=%s" % id
        res_dirt2 = rq.get(requrl_orgdt).json()
        total_res_dirt["Star"].append(res_dirt2["data"]["star"])
        total_res_dirt["OryUrl"].append(res_dirt2["data"]["shareUrl"])

    print("step2:Category %s is finish!" % res_cate_list_fa[index]["cate_name"])


columns_list = ["分类", "机构ID", "机构名称", "联系电话", "联系地址", "课程数", "星级", "机构URL"]
df_total = pd.DataFrame(total_res_dirt)
df_total.columns = columns_list
df_total.drop_duplicates(subset=["机构名称", "联系电话"], keep="first", inplace=True)
df_total.drop("机构ID", axis=1, inplace=True)
df_total.reset_index(drop=True)
df_total.index += 1

writer = pd.ExcelWriter(u"/Users/huangxingnai/to_excel/TEXue_App_Rep_20181109.xlsx")
df_total.to_excel(writer, sheet_name="TEXue_Org_List")
writer.save()
