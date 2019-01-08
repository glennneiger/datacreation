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

class PublishData(object):

    def __init__(self):
        self.path_datapoint = find_path() + '/data' + '/datapoint.xlsx'
        self.path_login = find_path() + '/data' + "/login.xlsx"
        self.path_parking = find_path() + '/data' + "/parking.xlsx"
        self.token = EX.get_key_value(self.path_login, get_login_sheet_name(), "access_token")
        self.headers = {"Content-Type": "application/json", "Access-Token": self.token}
        self.host = get_host()
        self.port = ""

    def parking_lot(self):
        """车场信息"""
        url = self.host + '/v2/service/iot/publish?sdk=2'
        print(url)
        id_lists = EX.get_key_values(self.path_parking, "parking_lot","id")
        parking_name_lists = EX.get_key_values(self.path_parking, "parking_lot", "parking_name")
        in_park_mount_lists = EX.get_key_values(self.path_parking, "parking_lot", "in_park_mount")
        out_park_mount_lists = EX.get_key_values(self.path_parking, "parking_lot", "out_park_mount")
        all_book_space_lists = EX.get_key_values(self.path_parking, "parking_lot", "all_book_space")
        regular_book_space_lists = EX.get_key_values(self.path_parking, "parking_lot", "regular_book_space")
        rest_book_space_lists = EX.get_key_values(self.path_parking, "parking_lot", "rest_book_space")
        parking_code_lists = EX.get_key_values(self.path_parking, "parking_lot", "parking_code")
        project_code_lists = EX.get_key_values(self.path_parking, "parking_lot", "project_code")
        rest_regular_book_space_lists = EX.get_key_values(self.path_parking, "parking_lot", "rest_regular_book_space")

        for i in range(len(id_lists)):
            body = {
                "service_id": "parking",
                "table": "parking_lot",
                "operation": "upsert",
                "data":{
                    "id":id_lists[i],
                    "parking_name":parking_name_lists[i],
                    "in_park_mount":in_park_mount_lists[i],
                    "out_park_mount":out_park_mount_lists[i],
                    "all_book_space":all_book_space_lists[i],
                    "regular_book_space":regular_book_space_lists[i],
                    "rest_book_space":rest_book_space_lists[i],
                    "parking_code":parking_code_lists[i],
                    "project_code":project_code_lists[i],
                    "rest_regular_book_space":rest_regular_book_space_lists[i]
                }
            }
            print(body)
            try:
                r = requests.post(url=url, json=body, headers=self.headers)
                if (r.status_code == 200):
                    print("数据发送成功！")
                    print(r.text)
                else:
                    print("请求失败,错误码：", r.status_code)
            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise

    def barrier_gate(self, pid):
        """道闸"""
        url = self.host + '/v2/service/iot/publish?sdk=2'
        print(url)
        id_lists = EX.get_key_values(self.path_parking, "barrier_gate", "id")
        park_id_lists = EX.get_key_values(self.path_parking, "barrier_gate", "park_id")
        gate_brand_lists = EX.get_key_values(self.path_parking, "barrier_gate", "gate_brand")
        gate_model_lists = EX.get_key_values(self.path_parking, "barrier_gate", "gate_model")
        gate_type_lists = EX.get_key_values(self.path_parking, "barrier_gate", "gate_type")
        gate_name_lists = EX.get_key_values(self.path_parking, "barrier_gate", "gate_name")
        gate_id_lists = EX.get_key_values(self.path_parking, "barrier_gate", "gate_id")
        gate_status_lists = EX.get_key_values(self.path_parking, "barrier_gate", "gate_status")
        gate_running_status_lists = EX.get_key_values(self.path_parking, "barrier_gate", "gate_running_status")
        is_online_lists = EX.get_key_values(self.path_parking, "barrier_gate", "is_online")

        for i in range(len(id_lists)):
            body = {
                "service_id": "parking",
                "table": "barrier_gate",
                "operation": "upsert",
                "product_id": pid,
                "data":{
                    "id":id_lists[i],
                    "park_id":park_id_lists[i],
                    "gate_brand":gate_brand_lists[i],
                    "gate_model":gate_model_lists[i],
                    "gate_type":gate_type_lists[i],
                    "gate_name":gate_name_lists[i],
                    "gate_id":gate_id_lists[i],
                    "gate_status":gate_status_lists[i],
                    "gate_running_status":gate_running_status_lists[i],
                    "is_online":is_online_lists[i]
                }
            }
            print(body)
            try:
                r = requests.post(url=url, json=body, headers=self.headers)
                if (r.status_code == 200):
                    print("数据发送成功！")
                    print(r.text)
                else:
                    print("创建失败,错误码：", r.status_code)
            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise

    def in_parking(self):
        """进场记录"""
        url = self.host + self.port + '/v2/service/iot/publish?sdk=2'

        id_lists = EX.get_key_values(self.path_parking, "in_parking", "id")
        park_id_lists = EX.get_key_values(self.path_parking, "in_parking", "park_id")
        event_id_lists = EX.get_key_values(self.path_parking, "in_parking", "event_id")
        gate_id_lists = EX.get_key_values(self.path_parking, "in_parking", "gate_id")
        car_no_lists = EX.get_key_values(self.path_parking, "in_parking", "car_no")
        car_type_lists = EX.get_key_values(self.path_parking, "in_parking", "car_type")
        in_photo_lists = EX.get_key_values(self.path_parking, "in_parking", "in_photo")
        in_time_lists = EX.get_key_values(self.path_parking, "in_parking", "in_time")
        open_mode_lists = EX.get_key_values(self.path_parking, "in_parking", "open_mode")
        in_note_lists = EX.get_key_values(self.path_parking, "in_parking", "in_note")
        car_no_card_lists = EX.get_key_values(self.path_parking, "in_parking", "car_no_card")
        car_no_color_lists = EX.get_key_values(self.path_parking, "in_parking", "car_no_color")
        parking_type_lists = EX.get_key_values(self.path_parking, "in_parking", "parking_type")
        car_brand_lists = EX.get_key_values(self.path_parking, "in_parking", "car_brand")
        ic_card_info_lists = EX.get_key_values(self.path_parking, "in_parking", "ic_card_info")
        fix_card_value_lists = EX.get_key_values(self.path_parking, "in_parking", "fix_card_value")
        remain_num_lists = EX.get_key_values(self.path_parking, "in_parking", "remain_num")
        remain_fix_num_lists = EX.get_key_values(self.path_parking, "in_parking", "remain_fix_num")
        parking_name_lists = EX.get_key_values(self.path_parking, "in_parking", "parking_name")

        for i in range(len(id_lists)):
            body = {
                "service_id": "parking",
                "table": "in_parking",
                "operation": "insert",
                "data":{
                    "id":id_lists[i],
                    "park_id":park_id_lists[i],
                    "event_id":event_id_lists[i],
                    "gate_id":gate_id_lists[i],
                    "car_no":car_no_lists[i],
                    "car_type":car_type_lists[i],
                    "in_photo":in_photo_lists[i],
                    "in_time":in_time_lists[i],
                    "open_mode":open_mode_lists[i],
                    "in_note":in_note_lists[i],
                    "car_no_card": car_no_card_lists[i],
                    "car_no_color": car_no_color_lists[i],
                    "parking_type": parking_type_lists[i],
                    "car_brand": car_brand_lists[i],
                    "ic_card_info": ic_card_info_lists[i],
                    "fix_card_value": fix_card_value_lists[i],
                    "remain_num": remain_num_lists[i],
                    "remain_fix_num": remain_fix_num_lists[i],
                    "parking_name": parking_name_lists[i]
                }
            }
            try:
                r = requests.post(url=url, json=body, headers=self.headers)
                if (r.status_code == 200):
                    print("数据发送成功！")
                    print(r.text)
                else:
                    print("创建失败,错误码：", r.status_code)
            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise

    def out_parking(self):
        """出场记录"""
        url = self.host + self.port + '/v2/service/iot/publish?sdk=2'

        id_lists = EX.get_key_values(self.path_parking, "out_parking", "id")
        park_id_lists = EX.get_key_values(self.path_parking, "out_parking", "park_id")
        gate_id_lists = EX.get_key_values(self.path_parking, "out_parking", "gate_id")
        event_id_lists = EX.get_key_values(self.path_parking, "out_parking", "event_id")
        car_no_lists = EX.get_key_values(self.path_parking, "out_parking", "car_no")
        out_photo_lists = EX.get_key_values(self.path_parking, "out_parking", "out_photo")
        out_time_lists = EX.get_key_values(self.path_parking, "out_parking", "out_time")
        parking_time_lists = EX.get_key_values(self.path_parking, "out_parking", "parking_time")
        open_mode_lists = EX.get_key_values(self.path_parking, "out_parking", "open_mode")
        ic_card_info_lists = EX.get_key_values(self.path_parking, "out_parking", "ic_card_info")
        pay_type_lists = EX.get_key_values(self.path_parking, "out_parking", "pay_type")
        ys_money_lists = EX.get_key_values(self.path_parking, "out_parking", "ys_money")
        ss_money_lists = EX.get_key_values(self.path_parking, "out_parking", "ss_money")
        open_note_lists = EX.get_key_values(self.path_parking, "out_parking", "open_note")
        in_parking_id_lists = EX.get_key_values(self.path_parking, "out_parking", "in_parking_id")
        pay_terminal_lists = EX.get_key_values(self.path_parking, "out_parking", "pay_terminal")
        in_time_lists = EX.get_key_values(self.path_parking, "out_parking", "in_time")
        fix_card_value_lists = EX.get_key_values(self.path_parking, "out_parking", "fix_card_value")
        parking_name_lists = EX.get_key_values(self.path_parking, "out_parking", "parking_name")

        for i in range(len(id_lists)):
            body = {
                "service_id": "parking",
                "table": "out_parking",
                "operation": "insert",
                "data":{
                    "id":id_lists[i],
                    "park_id":park_id_lists[i],
                    "event_id":event_id_lists[i],
                    "gate_id":gate_id_lists[i],
                    "car_no":car_no_lists[i],
                    "out_photo":out_photo_lists[i],
                    "out_time":out_time_lists[i],
                    "parking_time":parking_time_lists[i],
                    "open_mode":open_mode_lists[i],
                    "ic_card_info":ic_card_info_lists[i],
                    "pay_type":pay_type_lists[i],
                    "ys_money": ys_money_lists[i],
                    "ss_money": ss_money_lists[i],
                    "open_note": open_note_lists[i],
                    "in_parking_id": in_parking_id_lists[i],
                    "pay_terminal":pay_terminal_lists[i],
                    "in_time": in_time_lists[i],
                    "fix_card_value": fix_card_value_lists[i],
                    "parking_name": parking_name_lists[i]
                }
            }
            try:
                r = requests.post(url=url, json=body, headers=self.headers)
                if (r.status_code == 200):
                    print("数据发送成功！")
                    print(r.text)
                else:
                    print("创建失败,错误码：", r.status_code)
            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise

    def car_info(self):
        """车辆信息"""
        url = self.host + '/v2/service/iot/publish?sdk=2'
        print(url)
        id_lists = EX.get_key_values(self.path_parking, "car_info", "id")
        user_name_lists = EX.get_key_values(self.path_parking, "car_info", "user_name")
        user_sex_lists = EX.get_key_values(self.path_parking, "car_info", "user_sex")
        user_mobile_lists = EX.get_key_values(self.path_parking, "car_info", "user_mobile")
        car_status_lists = EX.get_key_values(self.path_parking, "car_info", "car_status")
        car_no_lists = EX.get_key_values(self.path_parking, "car_info", "car_no")
        parking_id_lists = EX.get_key_values(self.path_parking, "car_info", "parking_id")
        card_number_lists = EX.get_key_values(self.path_parking, "car_info", "card_number")
        car_brand_lists = EX.get_key_values(self.path_parking, "car_info", "car_brand")
        car_model_lists = EX.get_key_values(self.path_parking, "car_info", "car_model")
        car_no_color_lists = EX.get_key_values(self.path_parking, "car_info", "car_no_color")
        car_no_card_lists = EX.get_key_values(self.path_parking, "car_info", "car_no_card")
        record_date_lists = EX.get_key_values(self.path_parking, "car_info", "record_date")


        for i in range(len(id_lists)):
            body = {
                "service_id": "parking",
                "table": "car_info",
                "operation": "upsert",
                "data":{
                    "id":id_lists[i],
                    "user_name":user_name_lists[i],
                    "user_sex":user_sex_lists[i],
                    "user_mobile":user_mobile_lists[i],
                    "car_status":car_status_lists[i],
                    "car_no":car_no_lists[i],
                    "parking_id":parking_id_lists[i],
                    "card_number":card_number_lists[i],
                    "car_brand":car_brand_lists[i],
                    "car_model":car_model_lists[i],
                    "car_no_color":car_no_color_lists[i],
                    "car_no_card": car_no_card_lists[i],
                    "record_date": record_date_lists[i]
                }
            }
            print(body)
            try:
                r = requests.post(url=url, json=body, headers=self.headers)
                if (r.status_code == 200):
                    print("数据发送成功！")
                    print(r.text)
                else:
                    print("创建失败,错误码：", r.status_code)
            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise

    def charge_data(self):
        """收费数据"""
        url = self.host + self.port + '/v2/service/iot/publish?sdk=2'
        print(url)
        id_lists = EX.get_key_values(self.path_parking, "charge_data", "id")
        car_id_lists = EX.get_key_values(self.path_parking, "charge_data", "car_id")
        project_id_lists = EX.get_key_values(self.path_parking, "charge_data", "project_id")
        car_no_lists = EX.get_key_values(self.path_parking, "charge_data", "car_no")
        charge_date_lists = EX.get_key_values(self.path_parking, "charge_data", "charge_date")
        billcharge_start_lists = EX.get_key_values(self.path_parking, "charge_data", "billcharge_start")
        billcharge_end_lists = EX.get_key_values(self.path_parking, "charge_data", "billcharge_end")
        ys_money_lists = EX.get_key_values(self.path_parking, "charge_data", "ys_money")
        ss_money_lists = EX.get_key_values(self.path_parking, "charge_data", "ss_money")
        parking_id_lists = EX.get_key_values(self.path_parking, "charge_data", "parking_id")
        fix_card_value_lists = EX.get_key_values(self.path_parking, "charge_data", "fix_card_value")
        month_num_lists = EX.get_key_values(self.path_parking, "charge_data", "month_num")
        pay_terminal_lists = EX.get_key_values(self.path_parking, "charge_data", "pay_terminal")
        pay_type_lists = EX.get_key_values(self.path_parking, "charge_data", "pay_type")

        for i in range(len(id_lists)):
            body = {
                "service_id": "parking",
                "table": "charge_data",
                "operation": "insert",
                "data":{
                    "id":id_lists[i],
                    "car_id":car_id_lists[i],
                    "project_id":project_id_lists[i],
                    "car_no":car_no_lists[i],
                    "charge_date":charge_date_lists[i],
                    "billcharge_start":billcharge_start_lists[i],
                    "billcharge_end":billcharge_end_lists[i],
                    "ys_money":ys_money_lists[i],
                    "ss_money":ss_money_lists[i],
                    "parking_id":parking_id_lists[i],
                    "fix_card_value":fix_card_value_lists[i],
                    "month_num": month_num_lists[i],
                    "pay_terminal": pay_terminal_lists[i],
                    "pay_type":pay_type_lists[i]
                }
            }
            print(body)
            try:
                r = requests.post(url=url, json=body, headers=self.headers)
                if (r.status_code == 200):
                    print("数据发送成功！")
                    print(r.text)
                else:
                    print("创建失败,错误码：", r.status_code)
            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise

    def abnormal_open_info(self, pid):
        """异常开闸记录"""
        url = self.host +  '/v2/service/iot/publish?sdk=2'
        print(url)
        id_lists = EX.get_key_values(self.path_parking, "abnormal_open_info","id")
        parking_id_lists = EX.get_key_values(self.path_parking, "abnormal_open_info", "parking_id")
        gate_id_lists = EX.get_key_values(self.path_parking, "abnormal_open_info", "gate_id")
        abnormal_open_type_lists = EX.get_key_values(self.path_parking, "abnormal_open_info", "abnormal_open_type")
        open_date_lists = EX.get_key_values(self.path_parking, "abnormal_open_info", "open_date")
        open_reason_lists = EX.get_key_values(self.path_parking, "abnormal_open_info", "open_reason")

        for i in range(len(id_lists)):
            body = {
                "service_id": "parking",
                "table": "abnormal_open_info",
                "operation": "insert",
                "product_id": pid,
                "data":{
                    "id":id_lists[i],
                    "parking_id":parking_id_lists[i],
                    "gate_id":gate_id_lists[i],
                    "abnormal_open_type":abnormal_open_type_lists[i],
                    "open_date":open_date_lists[i],
                    "open_reason":open_reason_lists[i]
                }
            }
            print(body)
            try:
                r = requests.post(url=url, json=body, headers=self.headers)
                if (r.status_code == 200):
                    print("数据发送成功！")
                    print(r.text)
                else:
                    print("创建失败,错误码：", r.status_code)
            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise

    def add_parking(self):
        """新增车场接入"""
        url = self.host + '/v2/parks/parkinglots/a8fe7e9d3003b4897df776e73e409c0a/save'
        print(url)
        body = {
            "gate_product_id": "1607d2b8635a00011607d2b8635a1a01",   # 道闸产品id
            "gate_product_name": "道闸",                             # 道闸产品名称
            "id": "B_0066",                                          # 停车场ID(全平台唯一)
            "theam":"建研中心E区停车场",
            "create_date": "2019-01-05 19:39"               # 登记日期
        }
        print(body)
        try:
            r = requests.post(url=url, json=body, headers=self.headers)
            if (r.status_code == 200):
                print("数据发送成功！")
                print(r.text)
            else:
                print("创建失败,错误码：", r.status_code)
        except Exception:
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            raise


if __name__ == '__main__':
    pd = PublishData()
    # pd.parking_lot()            # 车场信息
    # pd.barrier_gate("1607d2b8635a00011607d2b8635a1a01")           # 道闸
    pd.car_info()               # 车辆信息
    pd.charge_data()            # 收费数据
    pd.in_parking()             # 进场记录
    pd.out_parking()            # 出场记录
    # pd.abnormal_open_info("1607d2b8635a00011607d2b8635a1a01")     # 异常开闸记录
    # pd.add_parking()             #新增车场接入



