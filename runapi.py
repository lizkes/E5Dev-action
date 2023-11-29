# -*- coding: UTF-8 -*-
import os
import json
import sys
import time
import random
import requests as req

# 配置选项，自由选择
config_list = {
    '运行轮数': random.randint(1, 3),
    '每轮随机延迟': [0, 180],
    'API随机延时': [0, 30],
    'API最少调用数量': 4,
}

# API列表
# 参考https://developer.microsoft.com/zh-cn/graph/graph-explorer
api_list = [
    # 用户
    # User.ReadWrite.All
    r'https://graph.microsoft.com/v1.0/me',
    r'https://graph.microsoft.com/v1.0/me/directReports',
    # Outlook邮件
    # Mail.ReadWrite
    r'https://graph.microsoft.com/v1.0/me/messages',
    r"https://graph.microsoft.com/v1.0/me/messages?$filter=importance eq 'high'",
    # Outlook日历
    # Calendars.ReadWrite
    r'https://graph.microsoft.com/v1.0/me/calendars',
    # 个人联系人
    # Contacts.ReadWrite
    r'https://graph.microsoft.com/v1.0/me/contacts',
    # OneDrive
    # Files.ReadWrite.All
    r'https://graph.microsoft.com/v1.0/me/drive/recent',
    r'https://graph.microsoft.com/v1.0/me/drive/root/children',
    # OneNote
    # Notes.ReadWrite.All
    r'https://graph.microsoft.com/v1.0/me/onenote/notebooks',
    # 应用程序
    # Application.ReadWrite.All
    r'https://graph.microsoft.com/v1.0/applications?$count=true',
    # 微软代办
    # Tasks.ReadWrite
    r'https://graph.microsoft.com/v1.0/me/todo/lists',
]

# 获取环境变量，否则抛出错误
def get_env_or_err(env):
    result = os.getenv(env)
    if result:
        return result
    else:
        print(f'错误，无法获取到环境变量: {env}')
        sys.exit(1)

# 微软access_token获取
def get_access_token():
    response = req.post(
        'https://login.microsoftonline.com/common/oauth2/v2.0/token',
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
        },
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': get_env_or_err('MS_TOKEN'),
            'client_id': get_env_or_err('CLIENT_ID'),
            'client_secret': get_env_or_err('CLIENT_SECRET'),
            'redirect_uri': 'http://localhost:53682/'
        },
    )
    jsontxt = json.loads(response.text)
    if 'access_token' in jsontxt:
        print(f'access_token获取成功')
    else:
        print(f'access_token获取失败\n请检查secret里 CLIENT_ID , CLIENT_SECRET , MS_TOKEN 格式与内容是否正确，然后重新设置')
    return jsontxt['access_token']

# 调用API
def runapi(run_api_indexes):
    for index, run_api_index in enumerate(run_api_indexes):
        prefix_message = f'[{index+1}/{len(run_api_indexes)}]'
        print(f'{prefix_message}准备调用API: {api_list[run_api_index]}')
        if config_list['API随机延时']:
            api_delay = rolldelay(config_list['API随机延时'])
            print(f'{prefix_message}本次API调用延迟 {str(api_delay)} 秒')
            time.sleep(api_delay)
        try:
            response = req.get(
                api_list[run_api_index],
                headers={
                    'Authorization': access_token,
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
                },
            )
            if response.status_code == req.codes.ok:
                print(f'{prefix_message}API调用成功, 状态码:{response.status_code}')
            else:
                response.raise_for_status()
        except req.exceptions.RequestException as e:
            print(f'{prefix_message}API调用失败, {e}')
            pass

# 随机生成要运行的API列表
def rollapi():
    run_api_indexes = []
    all_api_indexes = list(range(0, len(api_list)))
    run_api_indexes.extend(random.sample(all_api_indexes, random.randint(config_list['API最少调用数量'], len(api_list))))
    random.shuffle(run_api_indexes)
    return run_api_indexes

# 随机生成延迟
def rolldelay(delay_list):
    return random.randint(delay_list[0], delay_list[1])

# 实际运行
access_token = get_access_token()
print(f'本次运行 {str(config_list["运行轮数"])} 轮')
for run_round in range(0, config_list['运行轮数']):
    print(f'\n第 {str(run_round+1)} 轮启动')
    if config_list['每轮随机延迟']:
        round_delay = rolldelay(config_list['每轮随机延迟'])
        print(f'本轮延迟 {round_delay} 秒')
        time.sleep(round_delay)
    run_api_indexes = rollapi()
    print(f'本轮该应用运行{len(run_api_indexes)}个api')
    runapi(run_api_indexes)
    print(f'第 {str(run_round+1)} 轮结束')
