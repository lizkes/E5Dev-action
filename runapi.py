# -*- coding: UTF-8 -*-
import os
import requests as req
import json
import sys
import time
import random

app_num = int(os.getenv('APP_NUM', 1))
access_token_list = []
# 配置选项，自由选择
config_list = {
    '运行轮数': random.randint(0, 5),
    '每轮随机延迟': random.randint(0, 3000),
    'api随机延时': random.randint(0, 60),
    '账号随机延时': 0,
}
# '是否开启备用应用':'N','是否开启测试':'N'
api_list = [r'https://graph.microsoft.com/v1.0/me/',
            r'https://graph.microsoft.com/v1.0/users',
            r'https://graph.microsoft.com/v1.0/me/people',
            r'https://graph.microsoft.com/v1.0/groups',
            r'https://graph.microsoft.com/v1.0/me/contacts',
            r'https://graph.microsoft.com/v1.0/me/drive/root',
            r'https://graph.microsoft.com/v1.0/me/drive/root/children',
            r'https://graph.microsoft.com/v1.0/drive/root',
            r'https://graph.microsoft.com/v1.0/me/drive',
            r'https://graph.microsoft.com/v1.0/me/drive/recent',
            r'https://graph.microsoft.com/v1.0/me/drive/sharedWithMe',
            r'https://graph.microsoft.com/v1.0/me/calendars',
            r'https://graph.microsoft.com/v1.0/me/events',
            r'https://graph.microsoft.com/v1.0/sites/root',
            r'https://graph.microsoft.com/v1.0/sites/root/sites',
            r'https://graph.microsoft.com/v1.0/sites/root/drives',
            r'https://graph.microsoft.com/v1.0/sites/root/columns',
            r'https://graph.microsoft.com/v1.0/me/onenote/notebooks',
            r'https://graph.microsoft.com/v1.0/me/onenote/sections',
            r'https://graph.microsoft.com/v1.0/me/onenote/pages',
            r'https://graph.microsoft.com/v1.0/me/messages',
            r'https://graph.microsoft.com/v1.0/me/mailFolders',
            r'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
            r'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
            r'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
            r"https://graph.microsoft.com/v1.0/me/messages?$filter=importance eq 'high'",
            r'https://graph.microsoft.com/v1.0/me/messages?$search="hello world"',
            r'https://graph.microsoft.com/beta/me/messages?$select=internetMessageHeaders&$top',
            ]

# 微软access_token获取
def getmstoken(ms_token, app_index):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': ms_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'http://localhost:53682/'
    }
    html = req.post(
        'https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers
    )
    jsontxt = json.loads(html.text)
    if 'refresh_token' in jsontxt:
        print(f'应用 {str(app_index+1)} 的微软密钥获取成功')
    else:
        print(f'应用 {str(app_index+1)} 的微软密钥获取失败\n \
                请检查secret里 CLIENT_ID , CLIENT_SECRET , MS_TOKEN 格式与内容是否正确，然后重新设置')
    #refresh_token = jsontxt["refresh_token"]
    access_token = jsontxt["access_token"]
    return access_token

# 调用函数
def runapi(run_api_list, app_index):
    access_token = access_token_list[app_index]
    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    for run_api in run_api_list:
        try:
            if req.get(api_list[run_api], headers=headers).status_code == 200:
                print(f'第 {str(run_api)} 号api调用成功')
                if config_list["api随机延时"] != 0:
                    time.sleep(config_list["api随机延时"])
        except req.exceptions.RequestException as e:
            print(f'错误, {e}')
            pass

# 一次性获取access_token，降低获取率
for app_index in range(0, app_num):
    if app_index == 0:
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        ms_token = os.getenv('MS_TOKEN')
        access_token_list[app_index] = getmstoken(ms_token, app_index)
    else:
        client_id = os.getenv('CLIENT_ID_'+str(app_index))
        client_secret = os.getenv('CLIENT_SECRET_'+str(app_index))
        ms_token = os.getenv('MS_TOKEN_'+str(app_index))
        access_token_list[app_index] = getmstoken(ms_token, app_index)

def rollapi():
    # 随机api序列
    fixed_api = [0, 1, 5, 6, 20, 21]
    # 保证抽取到outlook,onedrive的api
    ex_api = [2, 3, 4, 7, 8, 9, 10, 22, 23, 24, 25,
            26, 27, 13, 14, 15, 16, 17, 18, 19, 11, 12]
    # 额外抽取填充的api
    fixed_api.extend(random.sample(ex_api, random.randint(0, 22)))
    random.shuffle(fixed_api)
    return fixed_api

# 实际运行
print(f'共 {str(app_num)} 个应用，每个应用运行 {str(config_list["运行轮数"])} 轮')
for run_round in range(0, config_list["运行轮数"]):
    if config_list["每轮随机延迟"] != 0:
        time.sleep(config_list["每轮随机延迟"])
    for app_index in range(0, app_num):
        if config_list["账号随机延时"] != 0:
            time.sleep(config_list["账号随机延时"])
        if app_index == 0:
            client_id = os.getenv('CLIENT_ID')
            client_secret = os.getenv('CLIENT_SECRET')
            print(f'\n应用 {str(app_index+1)} 的第 {str(run_round+1)} 轮')
            run_api_list = rollapi()
            runapi(run_api_list, app_index)
            print(f'本轮共运行{len(run_api_list)}个api')
        else:
            client_id = os.getenv('CLIENT_ID_'+str(app_index+1))
            client_secret = os.getenv('CLIENT_SECRET_'+str(app_index+1))
            print(f'\n应用 {str(app_index+1)} 的第 {str(run_round+1)} 轮')
            run_api_list = rollapi()
            runapi(run_api_list, app_index)
            print(f'本轮运行{len(run_api_list)}个api')
