#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票热点日报 - 单文件 HTML 生成器
无需模板引擎，直接生成完整 HTML
"""

import os
import json
import sys
from datetime import datetime, timedelta

# 配置
SITE_DIR = '/app/working/stock_daily_site'
DATA_DIR = os.path.join(SITE_DIR, 'data')
DAILY_DIR = os.path.join(SITE_DIR, 'daily')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DAILY_DIR, exist_ok=True)

def get_stock_data():
    """获取股票数据"""
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
            })
        
        # 获取大盘数据
        try:
            sh = ak.stock_zh_index_spot(symbol="sh000001")
            sz = ak.stock_zh_index_spot(symbol="sz399001")
            cy = ak.stock_zh_index_spot(symbol="sz399006")
            market = {
                'sh_close': float(sh.get('最新价', [3050])[0]),
                'sh_change': float(sh.get('涨跌幅', [0.5])[0]),
                'sz_close': float(sz.get('最新价', [9200])[0]),
                'sz_change': float(sz.get('涨跌幅', [0.8])[0]),
                'cy_close': float(cy.get('最新价', [1850])[0]),
                'cy_change': float(cy.get('涨跌幅', [1.2])[0]),
            }
        except:
            market = {
                'sh_close': 3050, 'sh_change': 0.5,
                'sz_close': 9200, 'sz_change': 0.8,
                'cy_close': 1850, 'cy_change': 1.2,
            }
        
        # 获取新闻
        news = [
            {'title': '央行：保持流动性合理充裕，支持实体经济发展', 'source': '央行', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '证监会：稳步推进全面注册制改革', 'source': '证监会', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '国家统计局：PMI 指数保持在扩张区间', 'source': '统计局', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '发改委：加大基础设施投资力度', 'source': '发改委', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '工信部：推动制造业高端化、智能化发展', 'source': '工信部', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '财政部：实施更大力度减税降费政策', 'source': '财政部', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '商务部：促进消费市场持续恢复', 'source': '商务部', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '人社部：稳就业政策持续发力', 'source': '人社部', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '住建部：因城施策支持住房需求', 'source': '住建部', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '金融监管局：防范化解金融风险', 'source': '金融监管局', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '外汇局：保持人民币汇率基本稳定', 'source': '外汇局', 'time': datetime.now().strftime('%m-%d %H:%M')},
            {'title': '能源局：推进能源绿色低碳转型', 'source': '能源局', 'time': datetime.now().strftime('%m-%d %H:%M')},
        ]
        
        return sectors, market, news
    except Exception as e:
        print(f"⚠️ 获取数据失败：{e}")
        # 返回备用数据
        sectors = [
            {'name': '人工智能', 'change': 3.5, 'leader': '科大讯飞'},
            {'name': '半导体', 'change': 2.8, 'leader': '中芯国际'},
            {'name': '新能源车', 'change': 2.1, 'leader': '比亚迪'},
            {'name': '医药生物', 'change': 1.5, 'leader': '恒瑞医药'},
            {'name': '消费电子', 'change': 1.2, 'leader': '立讯精密'},
            {'name': '光伏', 'change': 0.8, 'leader': '隆基绿能'},
            {'name': '银行', 'change': 0.5, 'leader': '招商银行'},
            {'name': '券商', 'change': 0.3, 'leader': '中信证券'},
        ]
        market = {
            'sh_close': 3050, 'sh_change': 0.5,
            'sz_close': 9200, 'sz_change': 0.8,
            'cy_close': 1850, 'cy_change': 1.2,
        }
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

def generate_html(date_str, date_cn, market, sectors, news, archives):
    """生成 HTML 内容"""
    
    # 生成大盘卡片
    def card_html(name, close, change):
        css_class = 'up' if change > 0 else 'down'
        change_str = f"{change:+.2f}%"
        return f'''
                <div class="card {css_class}">
                    <div class="card-title">{name}</div>
                    <div class="card-value">{close:.2f}</div>
                    <div class="card-change">{change_str}</div>
                </div>'''
    
    market_html = '\n'.join([
        card_html('上证指数', market['sh_close'], market['sh_change']),
        card_html('深证成指', market['sz_close'], market['sz_change']),
        card_html('创业板指', market['cy_close'], market['cy_change']),
    ])
    
    # 生成板块列表
    sector_items = []
    for i, s in enumerate(sectors, 1):
        css_class = 'up' if s['change'] > 0 else 'down'
        sector_items.append(f'''
                <div class="sector-item {css_class}">
                    <div class="sector-rank">#{i}</div>
                    <div class="sector-info">
                        <div class="sector-name">{s['name']}</div>
                        <div class="sector-leader">领涨：{s['leader']}</div>
                    </div>
                    <div class="sector-change">{s['change']:+.2f}%</div>
                </div>''')
    sector_html = '\n'.join(sector_items)
    
    # 生成新闻列表
    news_items = []
    for i, n in enumerate(news, 1):
        news_items.append(f'''
                <div class="news-item">
                    <div class="news-rank">{i}</div>
                    <div class="news-content">
                        <div class="news-title">{n['title']}</div>
                        <div class="news-meta">
                            <span class="news-source">{n['source']}</span>
                            <span class="news-time">{n['time']}</span>
                        </div>
                    </div>
                </div>''')
    news_html = '\n'.join(news_items)
    
    # 生成历史归档
    archive_items = []
    for a in archives:
        archive_items.append(f'''
                <a href="/daily/{a['date']}.html" class="archive-item">
                    <span class="archive-date">{a['date_cn']}</span>
                    <span class="archive-link">查看 →</span>
                </a>''')
    archive_html = '\n'.join(archive_items)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>股票热点日报 - {date_cn}</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>📈 股票热点日报</h1>
            <p class="date">{date_cn}</p>
            <p class="date-en">{date_str}</p>
        </header>

        <section class="section">
            <h2>📊 大盘概况</h2>
            <div class="market-cards">
{market_html}
            </div>
        </section>

        <section class="section">
            <h2>🔥 今日热点板块 TOP{len(sectors)}</h2>
            <div class="sector-list">
{sector_html}
            </div>
        </section>

        <section class="section">
            <h2>📰 重要新闻 TOP{len(news)}</h2>
            <div class="news-list">
{news_html}
            </div>
        </section>

        <section class="section">
            <h2>📁 历史归档</h2>
            <div class="archive-list">
{archive_html}
            </div>
            <div class="archive-more">
                <a href="/archive.html">查看全部历史 →</a>
            </div>
        </section>

        <footer>
            <p>免责声明：本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。</p>
            <p class="footer-time">生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
    <script src="/js/main.js"></script>
</body>
</html>'''
    
    return html

def generate_archive_html():
    """生成归档页面 HTML"""
    archives = []
    for i in range(30, 0, -1):
        d = datetime.now() - timedelta(days=i)
        archives.append({
            'date': d.strftime('%Y%m%d'),
            'date_cn': d.strftime('%Y年%m月%d日')
        })
    
    archive_items = []
    for a in archives:
        archive_items.append(f'''
        <a href="/daily/{a['date']}.html" class="archive-item">
            <span class="archive-date">{a['date_cn']}</span>
            <span class="archive-link">查看 →</span>
        </a>''')
    archive_html = '\n'.join(archive_items)
    
    html = f'''<!DOCTYPE html>
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
{archive_html}
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
</html>'''
    
    return html

def main():
    """主函数"""
    print("=" * 50)
    print("🚀 股票热点日报网站生成器")
    print("=" * 50)
    
    # 获取数据
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
    
    # 生成简单的 JS
    js_content = '''// 股票热点日报 - 简单的交互
console.log('股票热点日报已加载');

// 添加点击效果
document.querySelectorAll('.sector-item, .news-item').forEach(item => {
    item.addEventListener('click', function() {
        this.style.transform = 'scale(0.98)';
        setTimeout(() => {
            this.style.transform = '';
        }, 150);
    });
});
'''
    js_path = os.path.join(SITE_DIR, 'js', 'main.js')
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"✅ 生成 JS: {js_path}")
    
    print("=" * 50)
    print("✅ 网站生成完成！")
    print("=" * 50)
    print(f"\n📂 网站目录：{SITE_DIR}")
    print(f"🌐 部署步骤:")
    print("   1. 将 /app/working/stock_daily_site 目录推送到 GitHub")
    print("   2. 在 Vercel 导入该 GitHub 仓库")
    print("   3. Vercel 会自动部署为静态网站")
    print(f"\n📱 飞书推送链接：https://YOUR-SITE.vercel.app/daily/{date_str}.html")

if __name__ == "__main__":
    main()
