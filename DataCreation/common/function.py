# coding=utf-8

import logging,datetime
import os,re
import imaplib
import random,string


def find_path():
    '''
    返回工程所在路径
    :return:
    '''
    base_dir = os.path.dirname(os.path.dirname(__file__))
    base_dir = str(base_dir)
    base_dir = base_dir.replace('\\', '/')

    return base_dir


def find_files(path, rule):
    lists = []
    for f_path, dirs, files in os.walk(path):
        for fs in files:
            filename = os.path.join(f_path, fs)
            filename = str(filename)
            filename = filename.replace("\\", "/")
            if filename.endswith(rule):
                lists.append(filename)
    return lists


def log(massage):
    '''
    日志打印，将日志保存到report/log文件夹
    :param massage: 日志内容
    :return:
    '''
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    path = find_path() + '/report/log/'
    isexists = os.path.exists(path)
    if not isexists:
        os.makedirs(path)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=path+'/'+now+'.log')
    logging.info(massage)


def get_now_date():
    '''
    获取当前年月日
    :return:年-月-日
    '''
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    return now


def random_num():
    return random.randint(10000000, 99999999)


def random_string():
    return "".join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i',
                                      'h','g','f','e','d','c','b','a'], 8)).replace(" ","")

def random_string_mac():
    return "".join(random.sample(['d','c','b','a','1','2','3','4','5','6','7','8','9'], 6)).replace(" ","")




if __name__ == '__main__':
    # driver = webdriver.Firefox()
    # driver.get("http://admin-test.xlink.io:1081/#/auth/login")
    # scream_shot(driver, 'test1/test.jpg')
    # driver.quit()
    # print(get_now_date())
    # log("打印日志测试")
    # print(find_files(r"C:\Users\Administrator\Desktop\DataCreation\data",".py"))
    print(random_string())

