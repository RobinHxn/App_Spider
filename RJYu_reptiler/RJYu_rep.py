#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Python version: V3.7

Author: Robin&HXN

File version: V1.0

File name: RJYu_rep.py

Created on: 20181109

Resume:

"""

import requests as rq
import pandas as pd

res_cate_list_fa = []
total_res_dirt = {
    "Category": [],
    "OrgName": [],
    "ContactTel": [],
    "ContactAddr": [],
    "LessonNum": [],
    "GroupScore": [],
    "ServiceScore": [],
    "EncScore": [],
    "ProfScore": [],
    "CourseScore": []
    }

requrl_cate = u"https://api.runjiaoyu.com.cn/stu/v21/course/category/onlinelist?"
res_cate_dirt = rq.get(requrl_cate).json()

for data1 in res_cate_dirt["b"]:
    for i in range(0, len(data1["subCategories"])):
        res_cate_dirt_fa = {}
        res_cate_dirt_fa["cate_id"] = data1["subCategories"][i]["id"]
        res_cate_dirt_fa["cate_name"] = data1["subCategories"][i]["name"]
        res_cate_list_fa.append(res_cate_dirt_fa)

print("step1: Category is download!")

for index_cate in range(0, len(res_cate_list_fa)):
    requrl_pageNum = u"https://api.runjiaoyu.com.cn/stu/v21/search/course?" \
                     u"regionId=&pageNo=1&pageSize=10&cursor=&sortAsc=1&keyword=&subjectId=%s" \
                     u"&lon=120.1144048569242&lat=30.29912633875884&courseLevel=&sortType=1"\
                     % res_cate_list_fa[index_cate]["cate_id"]

    res_pageNum = rq.get(requrl_pageNum).json()
    res_cate_list_fa[index_cate]["page_total"] = res_pageNum["b"]["pageTotal"]
    # print("Category %s is finish!" % res_cate_list_fa[index_cate]["cate_name"])

print("step2: Total Category page number is download!")

for index in range(0, len(res_cate_list_fa)):
    group_list = []
    for page_num in range(1, int(res_cate_list_fa[index]["page_total"] + 1)):
        requrl_ser = u"https://api.runjiaoyu.com.cn/stu/v21/search/course?" \
                     u"regionId=&pageNo=%s&pageSize=10&cursor=&sortAsc=1&keyword=&subjectId=%s" \
                     u"&lon=120.1144048569242&lat=30.29912633875884&courseLevel=&sortType=1"\
                     % (page_num, res_cate_list_fa[index]["cate_id"])
        res_dirt = rq.get(requrl_ser).json()

        for group in res_dirt["b"]["data"]:
            group_list.append(group["groupId"])
            res_cate_list_fa[index]["group_list"] = group_list

print("step3: GroupId is download!")
print(res_cate_list_fa)

for index1 in range(0, len(res_cate_list_fa)):
    if int(res_cate_list_fa[index1]["page_total"]) != 0:
        for group_id in res_cate_list_fa[index1]["group_list"]:
            requrl_group = u"https://api.runjiaoyu.com.cn/stu/v21/group/smart/home?groupId=%s" % group_id
            res_group = rq.get(requrl_group).json()
            total_res_dirt["Category"].append(res_cate_list_fa[index1]["cate_name"])
            total_res_dirt["OrgName"].append(res_group["b"]["bizInfo"]["groupName"])
            total_res_dirt["ContactTel"].append(res_group["b"]["bizInfo"]["telephone"])
            total_res_dirt["ContactAddr"].append(res_group["b"]["bizInfo"]["address"])

            requrl_group_home = u"https://api.runjiaoyu.com.cn/stu/v21/group/smart/home?groupId=%s" % group_id
            res_group_home = rq.get(requrl_group_home).json()
            total_res_dirt["GroupScore"].append(res_group_home["b"]["bizInfo"]["grade"]["groupScore"])
            total_res_dirt["ServiceScore"].append(res_group_home["b"]["bizInfo"]["grade"]["serviceScore"])
            total_res_dirt["EncScore"].append(res_group_home["b"]["bizInfo"]["grade"]["envScore"])
            total_res_dirt["ProfScore"].append(res_group_home["b"]["bizInfo"]["grade"]["profScore"])
            total_res_dirt["CourseScore"].append(res_group_home["b"]["bizInfo"]["grade"]["courseScore"])

            requrl_group_curse = u"https://api.runjiaoyu.com.cn/stu/v21/course/group?" \
                                 u"pageNo=1&id=%s&subjectId=&pageSize=10&orderRule=1" % group_id
            res_group_course = rq.get(requrl_group_curse).json()
            total_res_dirt["LessonNum"].append(res_group_course["b"]["dataTotal"])

            print("Group URL: %s; Category: %s finish!" % (requrl_group, res_cate_list_fa[index1]["cate_name"]))
    else:
        pass

columns_list = ["分类", "机构名称", "联系电话", "联系地址", "课程数量",
                "综合评分", "服务态度", "教学环境", "专业水平", "课程内容"]
df_total = pd.DataFrame(total_res_dirt)
df_total.columns = columns_list
df_total.drop_duplicates(subset=["机构名称", "联系电话"], keep="first", inplace=True)
df_total.reset_index(drop=True)
df_total.index += 1

writer = pd.ExcelWriter(u"/Users/huangxingnai/to_excel/RJYu_App_Rep_20181112.xlsx")
df_total.to_excel(writer, sheet_name="RJYu_Org_List")
writer.save()
