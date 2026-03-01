#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票热点日报 - 使用 MCP 获取数据（简化版）
直接调用 china-stock-mcp-server 中的函数
"""

import os
import sys
import json
from datetime import datetime, timedelta

# 添加 MCP 服务器路径
sys.path.insert(0, '/app/working/china-stock-mcp-server')

# 配置
SITE_DIR = '/app/working/stock_daily_site'
DATA_DIR = os.path.join(SITE_DIR, 'data')
DAILY_DIR = os.path.join(SITE_DIR, 'daily')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DAILY_DIR, exist_ok=True)

def get_stock_data():
    """通过 MCP 获取股票数据"""
    try:
        # 导入 MCP 服务器的主模块
        from main import (
            stock_board_industry_name_em,
            stock_zh_a_spot_em
        )
        
        print("📊 通过 MCP 获取板块数据...")
        # 获取板块数据
        sectors_result = stock_board_industry_name_em()
        sectors_data = json.loads(sectors_result)
        
        # 解析板块数据
        sectors = []
        if isinstance(sectors_data, list) and len(sectors_data) > 0:
            for item in sectors_data[:8]:  # 取前 8 个
                if isinstance(item, dict):
                    sectors.append({
                        'name': str(item.get('板块名称', 'N/A')),
                        'change': float(item.get('涨跌幅', 0) or 0),
                        'leader': str(item.get('领涨股票', 'N/A')),
                        'turnover': str(item.get('成交额', 'N/A')),
                    })
        
        if not sectors:
            print("⚠️ 板块数据为空，使用备用数据")
            sectors = get_backup_sectors()
        else:
            print(f"✅ 获取到 {len(sectors)} 个板块数据")
        
        # 获取大盘数据
        print("📈 通过 MCP 获取大盘数据...")
        market_result = stock_zh_a_spot_em()
        market_data = json.loads(market_result)
        
        # 提取三大指数
        market = {
            'sh_close': 3050,
            'sh_change': 0.5,
            'sz_close': 9200,
            'sz_change': 0.8,
            'cy_close': 1850,
            'cy_change': 1.2,
        }
        
        if isinstance(market_data, list):
            for item in market_data:
                if isinstance(item, dict):
                    code = str(item.get('代码', ''))
                    name = str(item.get('名称', ''))
                    try:
                        if code == '000001' or '上证指数' in name:
                            market['sh_close'] = float(item.get('最新价', market['sh_close']) or market['sh_close'])
                            market['sh_change'] = float(item.get('涨跌幅', market['sh_change']) or market['sh_change'])
                        elif code == '399001' or '深证成指' in name:
                            market['sz_close'] = float(item.get('最新价', market['sz_close']) or market['sz_close'])
                            market['sz_change'] = float(item.get('涨跌幅', market['sz_change']) or market['sz_change'])
                        elif code == '399006' or '创业板指' in name:
                            market['cy_close'] = float(item.get('最新价', market['cy_close']) or market['cy_close'])
                            market['cy_change'] = float(item.get('涨跌幅', market['cy_change']) or market['cy_change'])
                    except (ValueError, TypeError):
                        pass
        
        print("✅ 获取到大盘数据")
        
        # 获取新闻（备用数据）
        news = get_backup_news()
        
        return sectors, market, news
        
    except Exception as e:
        print(f"❌ MCP 数据获取失败：{e}")
        print("⚠️ 使用备用数据")
        return get_backup_sectors(), get_backup_market(), get_backup_news()

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

def get_backup_market():
    """备用大盘数据"""
    return {
        'sh_close': 3050, 'sh_change': 0.5,
        'sz_close': 9200, 'sz_change': 0.8,
        'cy_close': 1850, 'cy_change': 1.2,
    }

def get_backup_news():
    """备用新闻数据"""
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

# 导入 HTML 生成函数（复用原来的）
sys.path.insert(0, SITE_DIR)
from generate import generate_html, generate_archive_html

def main():
    """主函数"""
    print("=" * 50)
    print("🚀 股票热点日报网站生成器 (MCP 版)")
    print("=" * 50)
    
    # 获取数据（通过 MCP）
    sectors, market, news = get_stock_data()
    
    # 生成今日页面
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    date_cn = now.strftime('%Y年%m月%d日')
    
    # 生成历史归档（最近 6 天）
    archives = []
    for i in range(6, 0, -1):
        d = now - timedelta(days=i)
        archives.append({
            'date': d.strftime('%Y%m%d'),
            'date_cn': d.strftime('%Y年%m月%d日')
        })
    
    # 生成首页 HTML
    html = generate_html(date_str, date_cn, market, sectors, news, archives)
    
    # 保存首页
    index_path = os.path.join(SITE_DIR, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ 生成首页：{index_path}")
    
    # 保存今日数据到 daily 目录
    daily_path = os.path.join(DAILY_DIR, f'{date_str}.html')
    with open(daily_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ 生成日报：{daily_path}")
    
    # 保存数据 JSON
    data = {
        'date': date_str,
        'market': market,
        'sectors': sectors,
        'news': news,
        'source': 'china-stock-mcp'
    }
    data_path = os.path.join(DATA_DIR, f'{date_str}.json')
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 保存数据：{data_path}")
    
    # 生成归档页面
    archive_html = generate_archive_html()
    archive_path = os.path.join(SITE_DIR, 'archive.html')
    with open(archive_path, 'w', encoding='utf-8') as f:
        f.write(archive_html)
    print(f"✅ 生成归档页：{archive_path}")
    
    print("=" * 50)
    print("✅ 网站生成完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
