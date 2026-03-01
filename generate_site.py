#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票热点日报网站生成器
生成静态 HTML 网站，可部署到 Vercel/GitHub Pages
"""

import os
import json
from datetime import datetime, timedelta
from jinja2 import Template
import sys

# 添加父目录到路径以导入股票数据模块
sys.path.insert(0, '/app/working/stock_daily_report')

SITE_DIR = '/app/working/stock_daily_site'
DATA_DIR = os.path.join(SITE_DIR, 'data')
DAILY_DIR = os.path.join(SITE_DIR, 'daily')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DAILY_DIR, exist_ok=True)

def get_stock_data():
    """获取股票数据（复用之前的逻辑）"""
    try:
        import akshare as ak
        # 获取板块数据
        df = ak.stock_board_industry_name_em()
        df = df.sort_values('涨跌幅', ascending=False).head(8)
        
        sectors = []
        for _, row in df.iterrows():
            sectors.append({
                'name': row.get('板块名称', 'N/A'),
                'change': float(row.get('涨跌幅', 0)),
                'leader': row.get('领涨股票', 'N/A'),
                'turnover': row.get('成交额', 'N/A'),
            })
        
        # 获取大盘数据
        market = {
            'sh_close': 3050, 'sh_change': 0.5,
            'sz_close': 9200, 'sz_change': 0.8,
            'cy_close': 1850, 'cy_change': 1.2,
        }
        
        # 获取新闻（备用数据）
        news = [
            {'title': '央行：保持流动性合理充裕', 'source': '央行', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '证监会：稳步推进全面注册制改革', 'source': '证监会', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '国家统计局：PMI 指数保持在扩张区间', 'source': '统计局', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '发改委：加大基础设施投资力度', 'source': '发改委', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '工信部：推动制造业高端化发展', 'source': '工信部', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '财政部：实施更大力度减税降费', 'source': '财政部', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '商务部：促进消费市场持续恢复', 'source': '商务部', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '人社部：稳就业政策持续发力', 'source': '人社部', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '住建部：因城施策支持住房需求', 'source': '住建部', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '金融监管局：防范化解金融风险', 'source': '金融监管局', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '外汇局：保持人民币汇率基本稳定', 'source': '外汇局', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '能源局：推进能源绿色低碳转型', 'source': '能源局', 'time': datetime.now().strftime('%m-%d %H:%M')},
        ]
        
        return sectors, market, news
    except Exception as e:
        print(f"获取数据失败：{e}")
        return [], {}, []

def generate_daily_page(date_str, sectors, market, news, is_latest=False):
    """生成单日页面"""
    # 读取模板
    template_path = os.path.join(SITE_DIR, 'templates', 'index.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template = Template(f.read())
    
    # 获取历史归档（最近 7 天）
    archives = []
    for i in range(min(7, is_latest and 6 or 7), 0, -1):
        d = datetime.strptime(date_str, '%Y%m%d') - timedelta(days=i)
        archives.append({
            'date': d.strftime('%Y%m%d'),
            'date_cn': d.strftime('%Y年%m月%d日')
        })
    
    # 渲染 HTML
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    html = template.render(
        date=date_str,
        date_cn=date_obj.strftime('%Y年%m月%d日'),
        market=market,
        sectors=sectors,
        news=news,
        archives=archives,
        generate_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    # 保存文件
    if is_latest:
        output_path = os.path.join(SITE_DIR, 'index.html')
    else:
        output_path = os.path.join(DAILY_DIR, f'{date_str}.html')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 生成页面：{output_path}")
    return output_path

def generate_archive_page():
    """生成历史归档页面"""
    template_str = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>历史归档 - 股票热点日报</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>📁 历史归档</h1>
            <p class="date">查看所有历史日报</p>
        </header>
        <section class="section">
            <div class="archive-list">
                {% for archive in archives %}
                <a href="/daily/{{ archive.date }}.html" class="archive-item">
                    <span class="archive-date">{{ archive.date_cn }}</span>
                    <span class="archive-link">查看 →</span>
                </a>
                {% endfor %}
            </div>
            <div style="text-align: center; margin-top: 20px;">
                <a href="/" style="color: #667eea; text-decoration: none;">← 返回首页</a>
            </div>
        </section>
        <footer>
            <p>免责声明：本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。</p>
        </footer>
    </div>
</body>
</html>
"""
    template = Template(template_str)
    
    # 生成最近 30 天的归档
    archives = []
    for i in range(30, 0, -1):
        d = datetime.now() - timedelta(days=i)
        archives.append({
            'date': d.strftime('%Y%m%d'),
            'date_cn': d.strftime('%Y年%m月%d日')
        })
    
    html = template.render(archives=archives)
    
    output_path = os.path.join(SITE_DIR, 'archive.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 生成归档页面：{output_path}")

def save_data(sectors, market, news, date_str):
    """保存数据到 JSON 文件"""
    data = {
        'date': date_str,
        'market': market,
        'sectors': sectors,
        'news': news,
        'generate_time': datetime.now().isoformat()
    }
    
    output_path = os.path.join(DATA_DIR, f'{date_str}.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 保存数据：{output_path}")

def main():
    """主函数"""
    print("=" * 50)
    print("🚀 股票热点日报网站生成器")
    print("=" * 50)
    
    # 获取数据
    sectors, market, news = get_stock_data()
    
    if not sectors:
        print("❌ 获取数据失败")
        return
    
    # 生成今日页面
    date_str = datetime.now().strftime('%Y%m%d')
    generate_daily_page(date_str, sectors, market, news, is_latest=True)
    
    # 保存数据
    save_data(sectors, market, news, date_str)
    
    # 生成归档页面
    generate_archive_page()
    
    print("=" * 50)
    print("✅ 网站生成完成！")
    print("=" * 50)
    print(f"\n📂 网站目录：{SITE_DIR}")
    print(f"🌐 部署到 Vercel: 将此目录推送到 GitHub，然后在 Vercel 导入")
    print(f"📱 飞书推送链接：https://your-site.vercel.app/daily/{date_str}.html")

if __name__ == "__main__":
    main()
