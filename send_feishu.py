#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票日报网站 - 飞书推送脚本
每天生成网站后自动发送飞书通知
"""

import requests
import json
from datetime import datetime

# 飞书配置
FEISHU_APP_ID = 'cli_a929700eb1789bd2'
FEISHU_APP_SECRET = 'GVgubHX4lb7j6x5ojyMP0ejvhheT6Pcz'
FEISHU_USER_ID = 'ou_4c219a0a98df4db783e4bc0cadc2ecb9'

# 网站域名
SITE_URL = 'https://stock-daily-personal.vercel.app'

def get_access_token():
    """获取飞书 access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=10)
        data = resp.json()
        
        if data.get('code') == 0:
            token = data.get('tenant_access_token')
            return token
        else:
            print(f"❌ 获取 token 失败：{data}")
            return None
    except Exception as e:
        print(f"❌ 请求失败：{e}")
        return None

def send_text_message(text):
    """发送文本消息"""
    token = get_access_token()
    if not token:
        return False
    
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    content = {
        "text": text
    }
    
    payload = {
        "receive_id": FEISHU_USER_ID,
        "msg_type": "text",
        "content": json.dumps(content)
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        result = resp.json()
        
        if result.get('code') == 0:
            print("✅ 飞书消息发送成功！")
            return True
        else:
            print(f"❌ 发送失败：{result}")
            return False
    except Exception as e:
        print(f"❌ 发送失败：{e}")
        return False

def send_daily_report():
    """发送日报推送"""
    now = datetime.now()
    date_cn = now.strftime('%Y年%m月%d日')
    date_str = now.strftime('%Y-%m-%d')
    weekday = now.strftime('%A')
    
    # 星期映射
    weekdays = {
        'Monday': '周一',
        'Tuesday': '周二',
        'Wednesday': '周三',
        'Thursday': '周四',
        'Friday': '周五',
        'Saturday': '周六',
        'Sunday': '周日'
    }
    weekday_cn = weekdays.get(weekday, '')
    
    text = f"""📈 股票热点日报 - {date_cn} {weekday_cn}

🔗 查看今日报告：{SITE_URL}/daily/{now.strftime('%Y%m%d')}.html

📊 内容包括：
• 大盘指数概况（上证/深证/创业板）
• 热点板块 TOP8
• 重要财经新闻 TOP12
• 历史归档可回溯

💡 提示：点击链接查看完整报告"""
    
    return send_text_message(text)

if __name__ == "__main__":
    print("=" * 50)
    print("📱 飞书推送 - 股票热点日报")
    print("=" * 50)
    success = send_daily_report()
    if success:
        print("\n✅ 推送完成！")
    else:
        print("\n❌ 推送失败")
    print("=" * 50)
