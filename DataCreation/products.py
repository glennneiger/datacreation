# encoding: utf-8

import os
import requests
import traceback
from common.function import find_path
from common import excel_unit as EX
from login import get_host,get_login_sheet_name
from common import ini_unit as INI

global false, true
false = False
true = True

class Product(object):

    def __init__(self):
        self.path_datapoint = find_path() + '/data' + '/datapoint.xlsx'
        self.path_login = find_path() + '/data' + "/login.xlsx"
        self.path_prd = find_path() + '/data' + "/products.xlsx"
        self.token = EX.get_key_value(self.path_login, get_login_sheet_name(), "access_token")
        self.headers = {"Content-Type": "application/json", "Access-Token": self.token}
        self.host = get_host()
        self.port = ""


    def create_products(self):
        """创建产品"""
        link_type = 1
        p_type = 0
        visible = 0
        prd_lists = []
        url = self.host + self.port + '/v2/product'
        lists = EX.load_product_data(self.path_prd,"手动导入产品信息")
        # lists = EX.load_product_data(self.path_prd, "Sheet1")  #测试
        for i in range(len(lists)):
            # 判断设备连接类型
            if lists[i][2] == "wifi设备":
                link_type = 1
            elif lists[i][2] == "Zigbee设备":
                link_type = 2
            elif lists[i][2] == "蓝牙设备":
                link_type = 3
            elif lists[i][2] == "蓝牙Mesh设备":
                link_type = 4
            elif lists[i][2] == "PC设备":
                link_type = 5

            # 判断产品类型
            if lists[i][3] == "其他":
                p_type = 0
            elif lists[i][3] == "消费电子":
                p_type = 1
            elif lists[i][3] == "智能家居":
                p_type = 2
            elif lists[i][3] == "智能安防":
                p_type = 3
            elif lists[i][3] == "商用/工控设备":
                p_type = 4
            elif lists[i][3] == "照明/电工":
                p_type = 5
            elif lists[i][3] == "生活电器":
                p_type = 6
            elif lists[i][3] == "暖通空气":
                p_type = 7

            # 判断可见权限
            if lists[i][5] == "企业可见":
                visible = 0
            elif lists[i][5] == "企业用户均可见":
                visible = 1

            body = {
                "name": lists[i][0],
                "description": lists[i][1],
                "link_type": link_type,
                "type": p_type,
                "os_type": lists[i][4],
                "visibility": visible
            }
            lists_temp = {"pname":"", "pid":"", "pkey":""}
            try:
                r = requests.post(url=url, json=body, headers=self.headers)
                if (r.status_code == 200):
                    res = eval(r.text)
                    print(res)
                    print("创建成功")
                    lists_temp["pname"] = res["name"]
                    lists_temp["pid"] = res["id"]
                    lists_temp["pkey"] = res["key"]
                    prd_lists.append(lists_temp)
                else:
                    print("创建失败,错误码：",r.status_code)
            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise
        if len(prd_lists) != 0:
            EX.write_product_data(self.path_prd,"自动导出产品信息",prd_lists) #将产品名称，pid，pkey写入excel
            # EX.write_product_data(self.path_prd, "Sheet2", prd_lists)  # 将产品名称，pid，pkey写入excel
            #将产品名称，pid，pkey写入ini文件
            j = 1
            for i in range(len(prd_lists)):
                section = 'DEVICE'+ str(j)
                INI.write_to_ini(section, "PRODUCTNAME", prd_lists[i]["pname"])
                INI.write_to_ini(section, "PRODUCTID", prd_lists[i]["pid"])
                INI.write_to_ini(section, "PRODUCTKEY", prd_lists[i]["pkey"])
                INI.write_to_ini(section, "DEVICELIMIT", "10")
                j += 1

    def delete_product(self):
        """删除产品"""
        pid_list = EX.load_product_data(self.path_prd, "自动导出产品信息")
        # pid_list = EX.load_product_data(self.path_prd, "Sheet2")
        type_tem = false
        for i in range(len(pid_list)):
            try:
                url = self.host + self.port + '/v2/product/' + pid_list[i][1]
                print(url)
                r = requests.delete(url=url, headers=self.headers)
                if (r.status_code == 200):
                    type_tem = true
                    print("删除成功")
                else:
                    print("删除失败,错误码：", r.status_code)
            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise
        if type_tem:
            EX.clear_product_data(self.path_prd, "自动导出产品信息")
        else:
            print("删除失败，未清除数据")

    def query_products(self):
        """查询产品信息"""
        pid_list = EX.load_product_data(self.path_prd, "自动导出产品信息")
        # pid_list = EX.load_product_data(self.path_prd, "Sheet2")
        lists = []
        if len(pid_list):
            for i in range(len(pid_list)):
                try:
                    url = self.host + self.port + '/v2/product/' + pid_list[i][1]
                    print(url)
                    r = requests.get(url=url, headers=self.headers)
                    if (r.status_code == 200):
                        res = eval(r.text)
                        print("查询成功")
                        print(res)
                        lists.append(res['name'])
                    else:
                        print("查询失败,错误码：", r.status_code)
                except Exception:
                    print('traceback.format_exc():\n%s' % traceback.format_exc())
                    raise
            return lists
        else:
            print("产品列表为空")


if __name__ == '__main__':
    pd = Product()
    pd.create_products()
    # pd.delete_product()
    # pd.query_products()


