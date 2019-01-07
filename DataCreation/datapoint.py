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

class Datapoint(object):

    def __init__(self):
        self.path_datapoint = find_path() + '/data' + '/datapoint.xlsx'
        self.path_login = find_path() + '/data' + "/login.xlsx"
        self.value_list = EX.load_data(self.path_datapoint,"Sheet3")
        self.token = EX.get_key_value(self.path_login, get_login_sheet_name(), "access_token")
        self.headers = {"Content-Type": "application/json", "Access-Token": self.token}
        self.host = get_host()
        self.port = ""

    def add_data_points(self):
        '''
        添加数据端点
        :return:
        '''
        source = 0
        type = 0
        read = 0
        url = self.host +  '/v2/product/' + self.value_list[0][0] + '/datapoint'
        print(url)
        for i in range(len(self.value_list)):
            # 判断数据来源
            if self.value_list[i][5] == u'应用设置':
                source = 1
            elif self.value_list[i][5] == u'设备上报':
                source = 3
            # 判断字段类型
            if self.value_list[i][6] == u'布尔':
                type = 1
            elif self.value_list[i][6] == u'单字节':
                type = 2
            elif self.value_list[i][6] == u'int16有符号':
                type = 3
            elif self.value_list[i][6] == u'int32有符号':
                type = 4
            elif self.value_list[i][6] == u'浮点':
                type = 5
            elif self.value_list[i][6] == u'字符串':
                type = 6
            elif self.value_list[i][6] == u'int16无符号':
                type = 8
            elif self.value_list[i][6] == u'int32无符号':
                type = 9
            # 判断是否可读写
            if self.value_list[i][10] == u'可读写':
                read = 1
            elif self.value_list[i][10] == u'只读':
                read = 0

            body = {
                "name": self.value_list[i][3],
                "field_name": self.value_list[i][4],
                "type": type,
                "index": self.value_list[i][1],
                "description": self.value_list[i][11],
                "symbol": self.value_list[i][9],
                "source": source,
                "is_read": true,
                "is_write": read,
                "min": self.value_list[i][7],
                "max": self.value_list[i][8]
            }
            print(body)
            try:
                r = requests.post(url=url, json=body, headers=self.headers)
                if (r.status_code != 200):
                    print("设置失败")
                    print(r.status_code)
            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise



    def get_all_data_points(self):
        '''
        获取所有数据端点
        :return:
        '''
        url = self.host + self.port + '/v2/product/' + self.value_list[0][0] + '/datapoints'
        try:
            r = requests.get(url=url, json={}, headers=self.headers)
            res = eval(r.text)
            return res
        except Exception:
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            raise


    def get_all_point_id(self,res):
        '''
        获取所有数据端点id
        :param res:
        :return:数据端点id
        '''
        ids = []
        for i in range(len(res)):
            ids.append(res[i]['id'])
        return ids

    def delete_all_data_point(self, list,pid):
        '''
        删除所有数据端点
        :return:
        '''

        id_list = list
        # 判断数据端点列表是否为空
        if len(id_list) == 0:
            print("数据端点列表为空，不需要删除")
            return

        for i in id_list:
            url = self.host + self.port + '/v2/product/' + pid + '/datapoint/' + i
            try:
                r = requests.delete(url=url, json={}, headers=self.headers)
                if (r.status_code == 200):
                    print("删除成功")
                else:
                    print(r.status_code)
                    print("删除失败")
            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise


if __name__ == '__main__':
    dpt = Datapoint()
    dpt.add_data_points()

    # 删除数据端点
    # rest = dpt.get_all_data_points()
    # id_list = dpt.get_all_point_id(rest)
    # dpt.delete_all_data_point(id_list,"160fa8b7c74503e9160fa8b7c7450c01")



