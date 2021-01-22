# -*- coding: UTF-8 -*-
import os
import json
import sys
import time
import random
import requests as req

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
ms_token = os.getenv('MS_TOKEN')
access_token = getmstoken(ms_token)

# 配置选项，自由选择
config_list = {
    '运行轮数': random.randint(1, 10),
    '每轮随机延迟': [0, 300],
    'API随机延时': [0, 30],
    'API最少调用数量': 16,
}
# https://developer.microsoft.com/zh-cn/graph/graph-explorer
api_list = [
    # 开始使用
    r'https://graph.microsoft.com/v1.0/me',
    # 用户
    r'https://graph.microsoft.com/v1.0/me/directReports',
    r'https://graph.microsoft.com/v1.0/users/delta?$select=displayName,givenName,surname',
    # 组
    r'https://graph.microsoft.com/v1.0/groups',
    r'https://graph.microsoft.com/v1.0/groups/delta?$select=displayName,description',
    # Outlook邮件
    r"https://graph.microsoft.com/v1.0/me/messages?$filter=importance eq 'high'",
    r'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
    r'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
    # Outlook日历
    r'https://graph.microsoft.com/v1.0/me/calendars',
    r'https://graph.microsoft.com/v1.0/me/events?$select=subject,body,bodyPreview,organizer,attendees,start,end,location',
    # 个人联系人
    r'https://graph.microsoft.com/v1.0/me/contacts',
    # OneDrive
    r'https://graph.microsoft.com/v1.0/me/drive',
    r'https://graph.microsoft.com/v1.0/me/drive/root',
    r'https://graph.microsoft.com/v1.0/me/drive/root/children',
    # Planner
    r'https://graph.microsoft.com/v1.0/me/planner/tasks',
    # 见解
    r'https://graph.microsoft.com/v1.0/me/insights/trending',
    # 人脉
    r'https://graph.microsoft.com/v1.0/me/people',
    # 人员
    r'https://graph.microsoft.com/v1.0/me/people/?$search=j',
    # 拓展
    r'https://graph.microsoft.com/v1.0/schemaExtensions',
    # OneNote
    r'https://graph.microsoft.com/v1.0/me/onenote/notebooks',
    r'https://graph.microsoft.com/v1.0/me/onenote/pages',
    # SharePoint网站
    r'https://graph.microsoft.com/v1.0/sites/root',
    r'https://graph.microsoft.com/v1.0/sites/root/drives',
    # SharePoint列表
    r'https://graph.microsoft.com/v1.0/sites/root/lists',
    # Microsoft Teams
    r'https://graph.microsoft.com/v1.0/me/joinedTeams',
    # 安全性
    r'https://graph.microsoft.com/v1.0/security/alerts?$top=1',
    r'https://graph.microsoft.com/beta/security/secureScores?$top=5',
    # 应用程序
    r'https://graph.microsoft.com/v1.0/applications?$count=true',
    # 微软代办
    r'https://graph.microsoft.com/v1.0/me/todo/lists',
    # 标识与访问
    r'https://graph.microsoft.com/v1.0/applicationTemplates',
]

# 微软access_token获取
def getmstoken(ms_token):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
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
    if 'access_token' in jsontxt:
        print(f'access_token获取成功')
    else:
        print(f'access_token获取失败\n请检查secret里 CLIENT_ID , CLIENT_SECRET , MS_TOKEN 格式与内容是否正确，然后重新设置')
    access_token = jsontxt['access_token']
    return access_token

# 调用API
def runapi(run_api_indexes):
    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    }
    for run_api_index in run_api_indexes:
        print(f'准备调用API: {api_list[run_api_index]}')
        if config_list['API随机延时']:
            api_delay = rolldelay(config_list['API随机延时'])
            print(f'本次API调用延迟 {str(api_delay)} 秒')
            time.sleep(api_delay)
        try:
            response = req.get(api_list[run_api_index], headers=headers)
            if response.status_code == req.codes.ok:
                print(f'API调用成功, 状态码:{response.status_code}')
            else:
                response.raise_for_status()
        except req.exceptions.RequestException as e:
            print(f'API调用失败, {e}')
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
print(f'本次运行 {str(config_list["运行轮数"])} 轮')
for run_round in range(0, config_list['运行轮数']):
    print(f'\n\n第 {str(run_round+1)} 轮启动')
    if config_list['每轮随机延迟']:
        round_delay = rolldelay(config_list['每轮随机延迟'])
        print(f'本轮延迟 {round_delay} 秒')
        time.sleep(round_delay)
    run_api_indexes = rollapi()
    print(f'本轮该应用运行{len(run_api_indexes)}个api')
    runapi(run_api_indexes)
    print(f'\n第 {str(run_round+1)} 轮结束')
