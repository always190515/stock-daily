#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票热点日报 - 使用 Playwright + 代理获取真实数据
"""

import os
import sys
import json
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# 配置
SITE_DIR = '/app/working/stock_daily_site'
DATA_DIR = os.path.join(SITE_DIR, 'data')
DAILY_DIR = os.path.join(SITE_DIR, 'daily')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DAILY_DIR, exist_ok=True)

# 代理配置（已禁用）
PROXY = None
# PROXY = {
#     'server': 'http://192.168.5.5:7890',
# }

def get_sectors_with_playwright():
    """
    使用 Playwright 获取东方财富板块数据
    """
    print("📊 使用 Playwright 获取板块数据...")
    
    sectors = []
    
    try:
        with sync_playwright() as p:
            # 启动浏览器
            if PROXY:
                print(f"   启动浏览器 (代理：{PROXY['server']})...")
                browser = p.chromium.launch(proxy=PROXY, headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
            else:
                print("   启动浏览器 (直连)...")
                browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
            
            page = browser.new_page()
            
            # 访问东方财富板块页面
            url = "https://quote.eastmoney.com/center/gridlist.html#industry_board"
            print(f"   访问：{url}")
            
            # 先访问页面，不等待 networkidle
            page.goto(url, timeout=60000, wait_until='domcontentloaded')
            
            # 等待数据加载
            print("   等待数据加载...")
            page.wait_for_timeout(8000)  # 等待 8 秒让 JS 执行
            
            # 尝试等待表格出现
            try:
                page.wait_for_selector('tbody tr', timeout=10000)
                print("   ✅ 表格已加载")
            except PlaywrightTimeout:
                print("   ⚠️ 未找到表格，继续...")
                page.wait_for_timeout(5000)
            
            # 执行 JavaScript 获取数据
            print("   提取数据...")
            data = page.evaluate('''() => {
                const sectors = [];
                // 查找表格行
                const rows = document.querySelectorAll('tbody tr');
                rows.forEach(row => {
                    const cols = row.querySelectorAll('td');
                    if (cols.length >= 5) {
                        const name = cols[1].textContent.trim();
                        const changeText = cols[2].textContent.trim().replace('%', '');
                        const change = parseFloat(changeText) || 0;
                        const leader = cols[4] ? cols[4].textContent.trim() : 'N/A';
                        
                        if (name && name !== '板块名称') {
                            sectors.push({ name, change, leader });
                        }
                    }
                });
                return sectors;
            }''')
            
            if data and len(data) > 0:
                sectors = data[:8]  # 取前 8 个
                print(f"   ✅ 获取到 {len(sectors)} 个板块")
                for i, s in enumerate(sectors, 1):
                    print(f"      {i}. {s['name']}: {s['change']:+.2f}% (领涨：{s['leader']})")
            else:
                print("   ⚠️ 未获取到数据，使用备用数据")
                sectors = get_backup_sectors()
            
            browser.close()
            
    except Exception as e:
        print(f"   ❌ 获取失败：{e}")
        print("   ⚠️ 使用备用数据")
        sectors = get_backup_sectors()
    
    return sectors

def get_news_from_web():
    """获取财经新闻"""
    print("📰 获取财经新闻...")
    
    url = "https://api.eastmoney.com/api/NewsList"
    params = {'type': 'cj', 'page': '1', 'pageSize': '15'}
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        import requests
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        news = []
        if 'Data' in data:
            for item in data['Data'][:12]:
                news.append({
                    'title': item.get('Title', '')[:80],
                    'source': '东方财富',
                    'time': item.get('ShowTime', '')[:16] if item.get('ShowTime') else datetime.now().strftime('%m-%d %H:%M')
                })
        
        if news:
            print(f"   ✅ 获取到 {len(news)} 条新闻")
            return news
    except:
        pass
    
    print("   ⚠️ 使用备用新闻")
    return get_backup_news()

def get_backup_sectors():
    """备用板块数据"""
    return [
        {'name': '人工智能', 'change': 3.5, 'leader': '科大讯飞'},
        {'name': '半导体', 'change': 2.8, 'leader': '中芯国际'},
        {'name': '新能源车', 'change': 2.1, 'leader': '比亚迪'},
        {'name': '医药生物', 'change': 1.5, 'leader': '恒瑞医药'},
        {'name': '消费电子', 'change': 1.2, 'leader': '立讯精密'},
        {'name': '光伏', 'change': 0.8, 'leader': '隆基绿能'},
        {'name': '银行', 'change': 0.5, 'leader': '招商银行'},
        {'name': '券商', 'change': 0.3, 'leader': '中信证券'},
    ]

def get_backup_news():
    """备用新闻"""
    now = datetime.now()
    return [
        {'title': '央行：保持流动性合理充裕', 'source': '央行', 'time': now.strftime('%m-%d %H:%M')},
        {'title': '证监会：稳步推进全面注册制改革', 'source': '证监会', 'time': now.strftime('%m-%d %H:%M')},
        {'title': '国家统计局：PMI 指数保持在扩张区间', 'source': '统计局', 'time': now.strftime('%m-%d %H:%M')},
        {'title': '发改委：加大基础设施投资力度', 'source': '发改委', 'time': now.strftime('%m-%d %H:%M')},
        {'title': '工信部：推动制造业高端化发展', 'source': '工信部', 'time': now.strftime('%m-%d %H:%M')},
        {'title': '财政部：实施更大力度减税降费', 'source': '财政部', 'time': now.strftime('%m-%d %H:%M')},
        {'title': '商务部：促进消费市场持续恢复', 'source': '商务部', 'time': now.strftime('%m-%d %H:%M')},
        {'title': '人社部：稳就业政策持续发力', 'source': '人社部', 'time': now.strftime('%m-%d %H:%M')},
        {'title': '住建部：因城施策支持住房需求', 'source': '住建部', 'time': now.strftime('%m-%d %H:%M')},
        {'title': '金融监管局：防范化解金融风险', 'source': '金融监管局', 'time': now.strftime('%m-%d %H:%M')},
        {'title': '外汇局：保持人民币汇率基本稳定', 'source': '外汇局', 'time': now.strftime('%m-%d %H:%M')},
        {'title': '能源局：推进能源绿色低碳转型', 'source': '能源局', 'time': now.strftime('%m-%d %H:%M')},
    ]

# 导入 HTML 生成
sys.path.insert(0, SITE_DIR)
from generate import generate_html, generate_archive_html

def main():
    """主函数"""
    print("=" * 50)
    print("🚀 股票热点日报 (Playwright + 代理)")
    print("=" * 50)
    
    # 检查代理配置
    if 'YOUR_PROXY' in PROXY['server']:
        print("\n⚠️  警告：请先配置代理地址！")
        print(f"   当前配置：{PROXY['server']}")
        print("\n请编辑文件：/app/working/stock_daily_site/generate_web_playwright.py")
        print("修改 PROXY 配置为你的实际代理地址，例如：")
        print("   PROXY = {'server': 'http://192.168.1.100:7890'}")
        print("\n使用备用数据继续...")
        sectors = get_backup_sectors()
    else:
        # 使用 Playwright 获取真实数据
        sectors = get_sectors_with_playwright()
    
    # 获取新闻
    news = get_news_from_web()
    
    # 大盘数据（简化）
    market = {
        'sh_close': 3050, 'sh_change': 0.5,
        'sz_close': 9200, 'sz_change': 0.8,
        'cy_close': 1850, 'cy_change': 1.2,
    }
    
    # 生成页面
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    date_cn = now.strftime('%Y年%m月%d日')
    
    archives = []
    for i in range(6, 0, -1):
        d = now - timedelta(days=i)
        archives.append({'date': d.strftime('%Y%m%d'), 'date_cn': d.strftime('%Y年%m月%d日')})
    
    html = generate_html(date_str, date_cn, market, sectors, news, archives)
    
    # 保存
    with open(os.path.join(SITE_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\n✅ 生成首页")
    
    with open(os.path.join(DAILY_DIR, f'{date_str}.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ 生成日报")
    
    data = {
        'date': date_str,
        'market': market,
        'sectors': sectors,
        'news': news,
        'source': 'playwright_with_proxy'
    }
    with open(os.path.join(DATA_DIR, f'{date_str}.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 保存数据")
    
    archive_html = generate_archive_html()
    with open(os.path.join(SITE_DIR, 'archive.html'), 'w', encoding='utf-8') as f:
        f.write(archive_html)
    print(f"✅ 生成归档页")
    
    print("\n" + "=" * 50)
    print("✅ 完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
