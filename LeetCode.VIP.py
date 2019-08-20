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
# TODO： not add CI test
# TODO: Pool(processes=-1), code run so slow.


from __future__ import print_function

import time
T1 = time.time()
import sys
import argparse
import requests
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
from multiprocessing import Pool
from urllib.parse import urljoin


if sys.version < "3":
    pass
else:
    pass


__author__="daidai"
__date__ = "2019.8.18 12:00"


INDEX_URL = "http://206.81.6.248:12306/leetcode/algorithm"
PROXY = {
    # "http": "http://127.0.0.1:1080",
    # "https": "https://127.0.0.1:1080",
}


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


def command():
    """
    # spider
    ./leetcode.VIP.py -u
    ./leetcode.VIP.py -update

    # problem
    ./leetcode.VIP.py -p
    ./leetcode.VIP.py -problem

    # company
    ./leetcode.VIP.py -c
    ./leetcode.VIP.py -company

    # proxy
    ./leetcode.VIP.py -proxy xxx
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument()

    args = parser.parse_args()
    # TODO: args


    # TODO: open in browser
    """
    mac:    open url
    linux:  x-www-browser url
    win:    cmd /c start url
    """


if __name__ == "__main__":
    problem_arr = generate_problem_page_url()
    problem_pd = pd.DataFrame(problem_arr, columns=["id", "title", "vip", "difficulty", "frequency"])
    problem_pd.to_csv("problem.csv", index=False)

    company_name_arr, company_problem_num_arr = get_company_infor()
    company_problem_id_arr = generate_company_page_url(company_name_arr)
    company_problem_id_pd = pd.DataFrame(company_problem_id_arr)
    company_problem_id_pd.rename(columns={company_problem_id_pd.columns[0]: "company"}, inplace=True)
    company_problem_id_pd.to_csv("company.csv", index=False)


    # temp
    """
    with open("index.html", "r", encoding="utf-8") as f:
        text_html = f.read()
        soup = BeautifulSoup(text_html, "html.parser")
        # print(soup.prettify())

        for page_num in soup.find_all(name="a", attrs="page-link active"):
            print(page_num.name, page_num["class"], page_num["href"], page_num.string)
        print(soup.find_all(name="a", attrs="page-link active")[-1].string)
    """


    print("Run Time: ", time.time() - T1)
