# encoding: utf-8

import os
import requests
import traceback
from common.function import find_path
from common import excel_unit as EX
from login import get_host,get_login_sheet_name

global false, true
false = False
true = True

class Devices(object):

    def __init__(self):
        self.path_device = find_path() + '/data' + '/devices.xlsx'
        self.path_login = find_path() + '/data' + "/login.xlsx"
        self.path_product = find_path() + '/data' + "/products.xlsx"
        self.device_info = EX.load_data(self.path_device,"设备注册")
        self.pid_lists = EX.load_data_by_column(self.path_product,"自动导出产品信息","pid")
        # self.pid_lists = EX.load_data_by_column(self.path_product, "Sheet2")
        self.token = EX.get_key_value(self.path_login, get_login_sheet_name(), "access_token")
        self.headers = {"Content-Type": "application/json", "Access-Token": self.token}
        self.host = get_host()
        self.port = ""

    def add_devices_single(self):
        '''
        给单个产品添加设备
        '''
        url = self.host + self.port + '/v2/product/' + self.device_info[0][0] + '/device'
        print(self.device_info[0][0])

        if len(self.device_info)==0:
            print("请在devices.xlsx文件中添加设备MAC")
            return

        for i in range(len(self.device_info)):
            body = {
                "mac": self.device_info[i][1],  # 设备MAC
                # "sn": self.device_info[i][2],           #设备SN，需要填写时配置
                "name": self.device_info[i][3],           #设备名称，需要填写时配置
                # "domain": self.device_info[i][4],
                # "tags": self.device_info[i][5]
            }
            # print(body)
            try:
                r = requests.post(url=url, json=body, headers=self.headers)
                if (r.status_code == 200):
                    print("设备MAC:%s,注册成功" % self.device_info[i][1])
                else:
                    print("注册失败，状态码：", r.status_code)

            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise


    def query_devices_by_product(self,pid):
        '''
        查询设备
        :return: 设备id
        '''
        devices_id = []
        url = self.host + self.port + '/v2/product/' + pid + '/devices'
        data = {"filter": ["id", "mac", "is_active", "active_date", "is_online", "sn", "last_login"],
                "order": {},
                "query": {},
                "limit": 200,
                "offset": 0
                }
        # 查询设备列表
        try:
            r = requests.post(url=url, json=data, headers=self.headers)
            if (r.status_code == 200):
                print("查询设备成功")
                res = eval(r.text)
                # 获取设备id
                for i in range(res['count']):
                    devices_id.append(res['list'][i]['id'])
            else:
                print("查询失败：", r.status_code)

        except Exception:
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            raise
        return devices_id

    def delete_devices_by_product(self, d_id, pid):
        '''
        删除单个产品下的设备
        :return:
        '''
        devices_id = d_id
        # 判断设备列表是否为空
        if len(devices_id) == 0:
            print("设备为空，不需要删除")
            return
        # 删除设备
        for i in range(len(devices_id)):
            id = str(devices_id[i])
            url = self.host + self.port + '/v2/product/' + pid + '/device/'+ id
            try:
                r = requests.delete(url=url, headers=self.headers)
                if (r.status_code == 200):
                    print("设备id%s,删除成功" %devices_id[i])
                else:
                    print("删除失败：", r.status_code)

            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise

    def add_devices_by_products(self,devices_num):
        """批量添加设备"""
        pid_len = len(self.pid_lists)
        mac_lists = EX.load_data_by_row_and_col(self.path_device, "MAC", pid_len, devices_num)
        name_lists = EX.load_data_by_row_and_col(self.path_device,"NAME1",1,10)
        # print(pid_len)
        # print(mac_lists)
        # print(name_lists)
        for i in range(len(self.pid_lists)):
            url = self.host + self.port + '/v2/product/' + str(self.pid_lists[i]) + '/device'
            # print(self.pid_lists[i])
            pname = EX.get_product_name(self.path_product, "Sheet2", self.pid_lists[i])
            print(len(mac_lists[0]))
            k = 0
            for j in range(len(mac_lists[0])):
                if k > len(name_lists[0])-1:
                    k = 0
                name = name_lists[0][k] + pname
                k += 1
                body = {
                    "mac": mac_lists[i][j],  # 设备MAC
                    "name": name             # 设备名称
                }
                try:
                    r = requests.post(url=url, json=body, headers=self.headers)
                    if (r.status_code == 200):
                        print("设备:%s,MAC:%s,注册成功" %(name, mac_lists[i][j]))
                    else:
                        print("注册失败，状态码：", r.status_code)

                except Exception:
                    print('traceback.format_exc():\n%s' % traceback.format_exc())
                    raise

    def query_devices_by_products(self):
        devices_id = []
        for i in range(len(self.pid_lists)):
            url = self.host + self.port + '/v2/product/' + self.pid_lists[i] + '/devices'
            data = {"filter": ["id", "mac", "is_active", "active_date", "is_online", "sn", "last_login"],
                    "order": {},
                    "query": {},
                    "limit": 200,
                    "offset": 0
                    }
            # 查询设备列表
            try:
                r = requests.post(url=url, json=data, headers=self.headers)
                if (r.status_code == 200):
                    print("查询设备成功")
                    res = eval(r.text)
                    # 获取设备id
                    for i in range(res['count']):
                        devices_id.append(res['list'][i]['id'])
                else:
                    print("查询失败：", r.status_code)

            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise
        return devices_id

    def delete_devices_by_products(self, d_id):
        '''
                删除单个产品下的设备
                :return:
                '''
        devices_id = d_id
        # 判断设备列表是否为空
        if len(devices_id) == 0:
            print("设备为空，不需要删除")
            return
        # 删除设备
        for j in range(len(self.pid_lists)):
            for i in range(len(devices_id)):
                id = str(devices_id[i])
                url = self.host + self.port + '/v2/product/' + self.pid_lists[j] + '/device/' + id
                try:
                    r = requests.delete(url=url, headers=self.headers)
                    if (r.status_code == 200):
                        print("设备id%s,删除成功" % devices_id[i])
                    else:
                        print("删除失败：", r.status_code)

                except Exception:
                    print('traceback.format_exc():\n%s' % traceback.format_exc())
                    raise


if __name__ == "__main__":
    device = Devices()
    # device.add_devices_single()
    # device.delete_devices_by_product(device.query_devices_by_product("160fa2b8416803e9160fa2b84168ea01"),
    #                                  "160fa2b8416803e9160fa2b84168ea01")

    #批量添加设备
    # device.add_devices_by_products(100)
    # device.delete_devices_by_products(device.query_devices_by_products())

