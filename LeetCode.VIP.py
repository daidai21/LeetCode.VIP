#!/usr/bin/env python3
# -*- coding:utf-8 -*-


# =============================================================================
# File Name: LeetCode.VIP.py
# Author: DaiDai
# Mail: daidai4269@aliyun.com
# Created Time: Thu Aug 15 17:50:36 2019
# =============================================================================


"""
Running this code get leetcode VIP information save to csv file and update every week.

URL: http://206.81.6.248:12306/leetcode/
"""


from __future__ import print_function

import time
T1 = time.time()
import os
import sys
import json
import argparse
import requests
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth',100)
from lxml import etree
from bs4 import BeautifulSoup
from multiprocessing import Pool
from urllib.parse import urljoin


__author__="daidai"
__date__ = "2019.8.18 12:00"


VERSION = 2 if sys.version < "3" else 3
INDEX_URL = "http://206.81.6.248:12306/leetcode/algorithm"
proxy_json_file = open("proxy.json", 'r')
PROXY = json.load(proxy_json_file)
proxy_json_file.close()
PLATFORM = sys.platform


def get_max_page_num_from_html(text_html):
    soup = BeautifulSoup(text_html, "html.parser")
    page_num_link_label = soup.find_all(name="a", attrs="page-link active")
    max_page_num = int(page_num_link_label[-1].string)
    return max_page_num


def get_problem_infor_from_html(text_html):
    dom = etree.HTML(text_html)

    id_arr = dom.xpath("//div/div/div/table/tbody/tr/td/text()")
    id_arr = [id for id in id_arr if '\n' not in id]  # clear other
    # print(id_arr, len(id_arr))
    title_arr = dom.xpath("//div/div/div/table/tbody/tr/td/a/text()")
    # print(title_arr, len(title_arr))
    vip_arr = dom.xpath("//div/div/div/table/tbody/tr/td/span/text()")
    vip_arr = [vip for vip in vip_arr if vip in ["Normal", "Prime"]]
    # print(vip_arr, len(vip_arr))
    difficulty_arr = dom.xpath("//div/div/div/table/tbody/tr/td/span/text()")
    difficulty_arr = [difficulty for difficulty in difficulty_arr if difficulty in ["Easy", "Medium", "Hard"]]
    # print(difficulty_arr, len(difficulty_arr))
    frequency_arr = dom.xpath("//div/div/div/table/tbody/tr/td/div/div/@style")
    frequency_arr = [frequency[7:-1] for frequency in frequency_arr]  # delete start "width: " and end '%'
    # print(frequency_arr, len(frequency_arr))

    err_msg = "Error: \
               get_problem_infor_from_html() \
               arr length is not same." + \
               "\n id_arr: " + str(len(id_arr)) + "\n" + str(id_arr) + \
               "\n title_arr: " + str(len(title_arr)) + "\n" + str(title_arr) + \
               "\n vip_arr: " + str(len(vip_arr)) + "\n" + str(vip_arr) + \
               "\n difficulty_arr: " + str(len(difficulty_arr)) + "\n" + str(difficulty_arr) + \
               "\n frequency_arr: " + str(len(frequency_arr)) + "\n" + str(frequency_arr)
    assert len(id_arr) == len(title_arr) == len(vip_arr) == len(difficulty_arr) == len(frequency_arr), err_msg

    return id_arr, title_arr, vip_arr, difficulty_arr, frequency_arr


def append_problem_infor(id_arr, title_arr, vip_arr, difficulty_arr, frequency_arr):
    problem_arr = []
    for id, title, vip, difficulty, frequency in zip(id_arr, title_arr, vip_arr, difficulty_arr, frequency_arr):
        problem_arr.append([id, title, vip, difficulty, frequency])
    return problem_arr


def generate_problem_page_url():
    problem_arr = []
    max_page_num = 1
    page_num = 1
    while page_num <= max_page_num:
        problem_page_url = "http://206.81.6.248:12306/leetcode/algorithm?page=" + str(page_num)
        r = requests.get(problem_page_url, timeout=2.0, proxies=PROXY)
        print(problem_page_url, r.status_code)
        err_msg = "get url error: " + str(problem_page_url)
        assert r.status_code == 200, err_msg
        if page_num == 1:
            max_page_num = get_max_page_num_from_html(r.text)
        id_arr, title_arr, vip_arr, difficulty_arr, frequency_arr = get_problem_infor_from_html(r.text)
        problem_arr += append_problem_infor(id_arr, title_arr, vip_arr, difficulty_arr, frequency_arr)
        page_num += 1
    return problem_arr


def get_company_infor():
    problem_page_url = "http://206.81.6.248:12306/leetcode/algorithm?page=" + str(1)
    r = requests.get(problem_page_url, timeout=2.0, proxies=PROXY)
    print(problem_page_url, r.status_code)
    text_html = r.text

    dom = etree.HTML(text_html)

    company_name_arr = dom.xpath("//div/div/div/div/a/text()")
    company_name_arr = [company_name.lstrip().rstrip() for company_name in company_name_arr if company_name.lstrip().rstrip() != '']  # delete space in the end and start
    # print(company_name_arr, len(company_name_arr))
    company_problem_num_arr = dom.xpath("//div/div/div/div/a/span/text()")
    # print(company_problem_num_arr, len(company_problem_num_arr))

    return company_name_arr, company_problem_num_arr


def generate_company_page_url(company_name_arr):
    company_problem_id_arr = []
    for company_name in company_name_arr:
        company_problem_id = [company_name]
        max_page_num = 1
        page_num = 1
        while page_num <= max_page_num:
            company_page_url = "http://206.81.6.248:12306/leetcode/" + company_name + "/algorithm?page=" + str(page_num)  # TODO: use url splice
            r = requests.get(company_page_url, timeout=2.0)
            print(company_page_url, r.status_code)
            err_msg = "get url error: " + str(company_page_url)
            assert r.status_code == 200, err_msg
            if page_num == 1:
                max_page_num = get_max_page_num_from_html(r.text)
            id_arr, _, _, _, _ = get_problem_infor_from_html(r.text)
            company_problem_id += id_arr
            page_num += 1
        company_problem_id_arr.append(company_problem_id)

    return company_problem_id_arr


def update_data():
    problem_arr = generate_problem_page_url()
    problem_pd = pd.DataFrame(problem_arr, columns=["id", "title", "vip", "difficulty", "frequency"])
    problem_pd.to_csv("problem.csv", index=False)

    company_name_arr, company_problem_num_arr = get_company_infor()
    company_problem_id_arr = generate_company_page_url(company_name_arr)
    company_problem_id_pd = pd.DataFrame(company_problem_id_arr)
    company_problem_id_pd.rename(columns={company_problem_id_pd.columns[0]: "company"}, inplace=True)
    company_problem_id_pd.to_csv("company.csv", index=False)


def print_search_infor(type=None, selection=None):
    problem_df = pd.read_csv("problem.csv")
    company_df = pd.read_csv("company.csv")
    if type == "problem":
        search_result = problem_df[problem_df["id"] == selection]
        if search_result.shape[0] == 0:
            print("search this problem id not found")
        else:
            print(search_result)
    elif type == "company":
        search_result = company_df[company_df["company"] == selection]
        if search_result.shape[0] == 0:
            print("search this company name not found")
        else:
            print(search_result.T)


def command():
    """
    ./leetcode.VIP.py -U --update         # update
    ./leetcode.VIP.py -P --problem        # problem
    ./leetcode.VIP.py -C --company        # company
    ./leetcode.VIP.py --proxy             # proxy
    ./leetcode.VIP.py -O --open-browser   # open browser
    ./leetcode.VIP.py show-id             # show problem information of id
    ./leetcode.VIP.py show-company        # show problem information of company name
    """
    description = "This is a simple shell tool about algorithms problem \
                   information of LeetCode. \n \
                   Github URL: https://github.com/daidai21/LeetCode.VIP"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-U", "--update", action="store_true", help=" run spider to download the newest data information.")
    parser.add_argument("-P", "--problem", action="store_true", help="show problem information.")
    parser.add_argument("-C", "--company", action="store_true", help="show company information.")
    parser.add_argument("--proxy", action="store_true", help="usage proxy.")
    parser.add_argument("-O", "--open-browser", type=int, action="store", help="open problem in browser.")
    parser.add_argument("-Sid", "--show-id", type=int, action="store", help="show problem information of id.")
    parser.add_argument("-Sc", "--show-company", type=str, action="store", help="show problem information of company name.")
    args = parser.parse_args()

    if args.update:  # FIXME
        if not args.proxy:
            global PROXY
            PROXY = None
        update_data()
    elif args.problem:
        problem_df = pd.read_csv("problem.csv")
        print(problem_df)
    elif args.company:
        company_df = pd.read_csv("company,csv")
        print(company_df)
    elif args.open_browser:
        problem_id = args.__dict__["open_browser"]
        problem_df = pd.read_csv("problem.csv")
        problem_name = problem_df[problem_df["id"] == problem_id]["title"].values[0]
        url = "https://leetcode.com/problems/" + '-'.join(problem_name.lower().split())
        if PLATFORM == "linux":
            os.system("x-www-browser " + url)
        elif PLATFORM == "":
            os.system("open " + url)
        elif PLATFORM == "win32":
            os.system("cmd /c start " + url)
        else:
            assert False, "Unrecognizable sys version."
    elif args.show_id:
        problem_id = args.__dict__["show_id"]
        print_search_infor(type="problem", selection=problem_id)
    elif args.show_company:
        company_name = args.__dict__["show_company"]
        print_search_infor(type="company", selection=company_name)
    else:
        os.system("./LeetCode.VIP.py --help")


if __name__ == "__main__":
    command()

    print("Run Time: ", time.time() - T1)
