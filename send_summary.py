#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送专业版早报摘要到飞书
"""

import requests
import json
from datetime import datetime

# 飞书配置
FEISHU_APP_ID = 'cli_a929700eb1789bd2'
FEISHU_APP_SECRET = 'GVgubHX4lb7j6x5ojyMP0ejvhheT6Pcz'
FEISHU_USER_ID = 'ou_4c219a0a98df4db783e4bc0cadc2ecb9'

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
            return data.get('tenant_access_token')
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

def send_daily_summary():
    """发送专业版早报摘要"""
    from enhanced_data_fetcher import ReportAnalyzer
    
    # 获取最新数据
    analyzer = ReportAnalyzer()
    report_data = analyzer.compile_daily_report()
    
    meta = report_data.get('meta', {})
    market = report_data.get('market_overview', {})
    sectors = report_data.get('active_sectors', [])
    summary = report_data.get('summary', {})
    outlook = report_data.get('outlook', {})
    sentiment = report_data.get('sentiment', {})
    external = report_data.get('external', {})
    
    # 构建消息
    now = datetime.now()
    date_str = now.strftime('%Y年%m月%d日')
    
    weekday_map = {'Monday': '周一', 'Tuesday': '周二', 'Wednesday': '周三', 
                   'Thursday': '周四', 'Friday': '周五', 'Saturday': '周六', 'Sunday': '周日'}
    weekday = weekday_map.get(now.strftime('%A'), '')
    
    main_line = summary.get('main_line', 'N/A')
    description = summary.get('description', 'N/A')
    
    sh = market.get('shanghai', {})
    sz = market.get('shenzhen', {})
    
    message = f"""📈 股票热点早报 - {date_str} {weekday}
━━━━━━━━━━━━━━━━━━━━━━

🎯 核心主线
{main_line}
驱动: {description}

📊 大盘指数
• 上证: {sh.get('close', 0):.2f} ({sh.get('change', 0):+.2f}%)
• 深证: {sz.get('close', 0):.2f} ({sz.get('change', 0):+.2f}%)

🔥 活跃板块TOP3"""

    for i, s in enumerate(sectors[:3], 1):
        message += f"\n{i}. {s.get('name', '')} {s.get('price_change', 0):+.2f}%"
        driver = s.get('driver', '')
        if driver:
            message += f"\n   🚀 {driver}"

    message += f"""

💰 资金方向: {summary.get('funding_direction', 'N/A')}

😊 市场情绪
• 热度: {sentiment.get('hot_level', 'N/A')}
• 涨停: {sentiment.get('涨停数量', 0)} | 跌停: {sentiment.get('跌停数量', 0)}
• 涨: {sentiment.get('上涨家数', 0)} | 跌: {sentiment.get('下跌家数', 0)}

🌏 外围市场"""

    us = external.get('us', {})
    for idx in us.get('indices', [])[:3]:
        message += f"\n• {idx.get('name', '')} {idx.get('change', '')}"

    message += f"""

🔮 今日前瞻
{outlook.get('trading_tips', '暂无建议')}

━━━━━━━━━━━━━━━━━━━━━━
🔗 查看完整报告: https://stock-daily-personal.vercel.app
📊 数据来源: AkShare | 版本: v2.0 专业版
⏰ 生成时间: {meta.get('generated_at', '')}"""
    
    return send_text_message(message)

if __name__ == "__main__":
    print("=" * 50)
    print("📱 发送专业版早报摘要到飞书")
    print("=" * 50)
    
    success = send_daily_summary()
    
    print("=" * 50)
    if success:
        print("✅ 发送完成！")
    else:
        print("❌ 发送失败")
    print("=" * 50)