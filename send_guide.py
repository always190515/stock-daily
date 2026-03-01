#!/usr/bin/env python3
"""
发送部署指南到飞书
"""
import requests
import json

FEISHU_APP_ID = 'cli_a929700eb1789bd2'
FEISHU_APP_SECRET = 'GVgubHX4lb7j6x5ojyMP0ejvhheT6Pcz'
FEISHU_USER_ID = 'ou_4c219a0a98df4db783e4bc0cadc2ecb9'

def get_token():
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    )
    data = resp.json()
    if data.get('code') == 0:
        return data.get('tenant_access_token')
    return None

def send():
    token = get_token()
    if not token:
        print("❌ 获取 token 失败")
        return
    
    text = """🎉 股票热点日报网站已准备就绪！

✅ 已完成：
• 网站代码生成（HTML/CSS/JS）
• Git 仓库初始化
• 部署文档编写
• 自动推送脚本

📤 下一步：推送到 GitHub

方式 1（推荐）：使用自动脚本
cd /app/working/stock_daily_site
python3 auto_push.py YOUR_TOKEN

方式 2：手动推送
git remote set-url origin https://always190515:TOKEN@github.com/always190515/stock-daily.git
git push -u origin main

🔑 获取 Token：
访问：https://github.com/settings/tokens/new
Token 名称：stock-daily-deploy
权限：勾选 'repo'
点击 'Generate token'，复制 token（ghp_开头）

📱 部署到 Vercel：
推送成功后，访问 https://vercel.com
用 GitHub 登录 -> New Project -> 选择 stock-daily -> Deploy

📖 完整指南：
/app/working/stock_daily_site/README_FINAL.md

需要帮助随时找我！🚀"""
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "receive_id": FEISHU_USER_ID,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }
    
    resp = requests.post(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        headers=headers, json=payload
    )
    result = resp.json()
    
    if result.get('code') == 0:
        print("✅ 飞书消息发送成功！")
        return True
    else:
        print(f"❌ 发送失败：{result}")
        return False

if __name__ == "__main__":
    send()
