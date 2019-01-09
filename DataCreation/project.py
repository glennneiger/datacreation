# encoding: utf-8

import os
import requests
import openpyxl
import traceback
from common.function import find_path
from common import excel_unit as EX
from login import get_host,get_login_sheet_name
from common import ini_unit as INI

global false, true
false = False
true = True

# 给排水，供配电
# list_pid = [
#     '1607d2b8418000011607d2b84180ea01',
#     '1607d2b8418000011607d2b84180ea05',
#     '1607d2b8418000011607d2b84180ea09',
#     '1607d2b8418000011607d2b84180ec01',
#     '1607d2b8418000011607d2b84180ec05',
#     '1607d2b8418000011607d2b84180ec09',
#     '1607d2b8418000011607d2b84180ec0d',
#     '1607d2b8418000011607d2b84180ec11',
#     '1607d2b8418000011607d2b84180ec15'
# ]    

# 暖通
# list_pid = [
#     '1607d2b8418000011607d2b84180ec19',
#     '1607d2b8418000011607d2b84180ee01',
#     '1607d2b8418000011607d2b84180ee05',
#     '1607d2b8418000011607d2b84180ee09',
#     '1607d2b8418000011607d2b84180ee0d',
#     '1607d2b8418000011607d2b84180ee11'
# ]
# 公共照明
# list_pid = [
#     '1607d2b8418000011607d2b84180ee15'
# ]

list_pid = [
	'1607d2b85dcb00011607d2b85dcbcc01',
	'1607d2b85dcb00011607d2b85dcbcc05',
	'1607d2b85dcb00011607d2b85dcbcc09',
	'1607d2b85dcb00011607d2b85dcbce01',
	'1607d2b85dcb00011607d2b85dcbce05',
	'1607d2b85dcb00011607d2b85dcbce09',
	'1607d2b85dcb00011607d2b85dcbce0d',
	'1607d2b85dcb00011607d2b85dcbce11',
	'1607d2b85dcb00011607d2b85dcbce15',
	'1607d2b85dcb00011607d2b85dcbce19',
	'1607d2b85dcb00011607d2b85dcbd001',
	'1607d2b85dcb00011607d2b85dcbd005',
	'1607d2b85dcb00011607d2b85dcbd009',
	'1607d2b85dcb00011607d2b85dcbd00d',
	'1607d2b85dcb00011607d2b85dcbd011',
	'1607d2b85dcb00011607d2b85dcbd015',
]

# 项目id
list_pj_id = [
	"a8fe7e9d3003b4897df776e73e409c0a" #建研中心
    # 'f143d556e24440698cba5350691b0c32',# 项目id,三坊世家
    # # 'bc2a570a764880e28035d6ae6af5d44e',# 项目id,人文
    # # '535566493312715d7a657a643075543d',# 项目id,冠亚
    # 'b4e5e82f77d55a8da2373a4b2b7bd897',# 项目id,外滩
    # 'c60a494c9153d130aaf4c2f23e48e213',# 项目id,江岸
    # '3bcd1667a7b3db79ee45d6920f8b9816',# 项目id,黎明迎春
    # # '4619ac61daeeda9e7f9554ae25ca13a2',# 项目id,广德明珠
    # '42f7f877993d575a78da128034940ed7',# 项目id,福华
    # # 'dba59ce5d41facaebccef596733d3204',# 项目id,广达
    # 'd68f9108a22fcb18b1f50cd36d60c21e',# 项目id,东方纽约
    # # '56a824e06ba0bc961399dd1c76d437fa',# 项目id,广安城
    # '409b7d6106f8d452350d3499d06f8e5a',# 项目id,福寿
    # # '83af1170764f87d5f28f7fced65d7b37',# 项目id,建新
    # '7922d0ee3dcaae5ae21933fee2ad3d46',# 项目id,蒲苇
    # '78363d02b15a53eb5fcfdd4aef5cc9be',# 项目id,双丰
    # '128766fa2a80226600322a79ad079d22' # 项目id,三源
]


list_num = [0,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95]
i_num = 0


class Projects(object):

    def __init__(self):
        self.path_login = find_path() + '/data' + "/login.xlsx"
        self.path_project = find_path() + '/data' + "/projects.xlsx"
        self.path_prd = find_path() + '/data' + "/products.xlsx"
        self.token = EX.get_key_value(self.path_login, get_login_sheet_name(), "access_token")
        self.headers = {"Content-Type": "application/json", "Access-Token": self.token}
        self.host = get_host()
        self.port = ""

    def query_organization_id(self):
        organization_id_lists = []
        url = self.host + self.port + '/v2/corp/organizations'
        body = {
            "offset":0,
            "limit":5,
            "filter": ["id", "name"],
            "query":{},
            "order":{}
        }
        try:
            r = requests.post(url=url,json=body, headers=self.headers)
            if (r.status_code == 200):
                print("查询项目组织成功")
                res = eval(r.text)
                # print(res)
                # 获取项目组织id
                if res['count']:
                    for i in range(5):
                        organization_id_lists.append(res['list'][i]['id'])
                else:
                    print("该成员账号下无组织架构或组织架构为空")
            else:
                print("查询失败：", r.status_code)
        except Exception:
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            raise
        print(organization_id_lists)
        return organization_id_lists

    def create_projects(self):
        organization_ids = self.query_organization_id()
        project_name_lists = EX.load_data_by_column(self.path_project, "项目信息", "项目名称")
        project_type_lists = EX.load_data_by_column(self.path_project, "项目信息", "项目类型")
        pj_lists = []
        p_type = 0
        for i in range(len(project_name_lists)):
            if project_type_lists[i] == "长租公寓":
                p_type = 1
            elif project_type_lists[i] == "智慧社区":
                p_type = 2
            elif project_type_lists[i] == "智慧家庭":
                p_type = 3
            elif project_type_lists[i] == "智慧路灯":
                p_type = 4
            elif project_type_lists[i] == "资产管理":
                p_type = 5
            elif project_type_lists[i] == "综合体":
                p_type = 6
            elif project_type_lists[i] == "标准类型":
                p_type = 7
            elif project_type_lists[i] == "联合办公":
                p_type = 8

            url = self.host + '/v2/realty-master-data/projects/project?project_type=' + str(p_type)
            print(url)
            body = {
                'name': project_name_lists[i],
                'organization_id': organization_ids[0]
            }
            print(body)
            pj_dict = {"pj_name": "", "pj_id": ""}
            try:
                r = requests.post(url=url, json=body, headers=self.headers)
                if (r.status_code == 200):
                    print("创建项目成功")
                    res = eval(r.text)
                    print(res)
                    pj_dict['pj_id'] = res['data']
                    pj_dict['pj_name'] = project_name_lists[i]
                    pj_lists.append(pj_dict)
                else:
                    print("创建项目失败：", r.status_code)
            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise
        if len(pj_lists):
            EX.write_project_data(self.path_project, "自动导出项目信息", pj_lists)

    def add_products_authorize(self):
        """添加产品授权"""
        project_id_lists = EX.load_data_by_column(self.path_project, "自动导出项目信息","pj_id")
        for i in range(len(project_id_lists)):
            url = self.host + '/v2/realty-master-data/authorizations/projects/' + project_id_lists[i] + '/products'
            product_id_lists = EX.load_data_by_column(self.path_prd, "自动导出产品信息","pid")
            print(product_id_lists)
            for j in range(len(product_id_lists)):
                data = {
                        "product_add_ids": [product_id_lists[j]]
                        }
                # 查询设备列表
                try:
                    r = requests.post(url=url, json=data, headers=self.headers)
                    if (r.status_code == 200):
                        print("产品授权成功")
                    else:
                        print("产品授权失败：", r.status_code)

                except Exception:
                    print('traceback.format_exc():\n%s' % traceback.format_exc())
                    raise

    def query_devices(self, pid):
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

    def add_devices_to_project(self, num):
        """关联设备到项目"""
        # project_id_lists = ["项目1","项目2","项目3"]
        # product_id_lists = ["产品1","产品2","产品3"]
        # devices = [["设备11", "设备12", "设备13", "设备14", "设备15", "设备16", "设备17", "设备18", "设备19", "设备110", "设备111", ],
        #            ["设备21", "设备22", "设备23", "设备24", "设备25", "设备26", "设备27", "设备28", "设备29", "设备210", "设备211", ],
        #            ["设备31", "设备32", "设备33", "设备34", "设备35", "设备36", "设备37", "设备38", "设备39", "设备310", "设备311", ]
        #            ]
        project_id_lists = EX.load_data_by_column(self.path_project, "自动导出项目信息", "pj_id")
        product_id_lists = EX.load_data_by_column(self.path_prd, "自动导出产品信息", "pid")
        counter = 0
        temp = 0
        for i in range(len(project_id_lists)):

            for j in range(len(product_id_lists)):
                devices_id = self.query_devices(product_id_lists[j])
                # devices_id = devices[j]
                print(devices_id)
                url = self.host + '/v2/realty-master-data/authorizations/projects/'+ project_id_lists[i] +'/products/' + product_id_lists[j] +'/devices'
                print(url)
                counter = counter + temp
                if (len(devices_id)-counter) < num:
                    num = (len(devices_id)-counter)

                for k in range(0, num):
                    data = {
                        "device_ids": [devices_id[counter + k]]
                    }
                    print(data)
                    try:
                        r = requests.post(url=url, json=data, headers=self.headers)
                        if (r.status_code == 200):
                            print("设备id%s,关联成功" % devices_id[counter])
                        else:
                            print("关联失败：", r.status_code)
                    except Exception:
                        print('traceback.format_exc():\n%s' % traceback.format_exc())
                        raise
            counter += num




if __name__ == '__main__':
    p = Projects()
    # p.query_organization_id()   # 查询组织ID
    # p.create_projects()         # 创建项目
    # p.add_products_authorize()  # 产品授权
    p.add_devices_to_project(4)   # 关联设备到项目


