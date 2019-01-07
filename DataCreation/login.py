# coding=utf-8

import requests
import os
from common import excel_unit as  EX
from common.function import find_path

curpath = os.path.dirname(os.path.realpath(__file__))


# login_sheet = "IOT"
# login_sheet = "PRO"
login_sheet = "DEV"


def get_host(sheet=login_sheet):
    path = find_path() + '/data' + "/login.xlsx"
    host = EX.get_key_value(path, sheet, "host")
    return  host


def get_login_sheet_name(sheet=login_sheet):
    return sheet


def login(sheet_name=login_sheet):
    path = find_path() + '/data' + "/login.xlsx"
    host = get_host(sheet_name)
    port = ""
    api = EX.get_key_value(path,sheet_name,"api")
    login_url = host + port + api
    username = EX.get_key_value(path,sheet_name,"username")
    password = EX.get_key_value(path,sheet_name,"password")
    data = {"account": username, "password": password}
    header = {"Content-Type": "application/json"}
    print(login_url)
    res = requests.post(login_url, json=data, headers=header)
    if res.status_code == 200:
        print("登录%s成功" % sheet_name)
    else:
        print("登录%s失败" % sheet_name)
    change_cont = eval(res.text)
    token = change_cont["access_token"]
    EX.write_key_value(path, sheet_name, "access_token", token)


if __name__ == "__main__":
    login()

