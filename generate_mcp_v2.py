#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票热点日报 - 专业版 v2.0
结合四层漏斗筛选逻辑的专业级早报生成器
"""

import os
import sys
import json
from datetime import datetime, timedelta
from enhanced_data_fetcher import ReportAnalyzer

# 配置
SITE_DIR = '/app/working/stock_daily_site'
DATA_DIR = os.path.join(SITE_DIR, 'data')
DAILY_DIR = os.path.join(SITE_DIR, 'daily')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DAILY_DIR, exist_ok=True)


def generate_professional_html(data: dict) -> str:
    """生成专业级HTML早报"""
    
    meta = data.get('meta', {})
    market = data.get('market_overview', {})
    sectors = data.get('active_sectors', [])
    money_flow = data.get('money_flow', {})
    news = data.get('news', [])
    sentiment = data.get('sentiment', {})
    external = data.get('external', {})
    summary = data.get('summary', {})
    outlook = data.get('outlook', {})
    
    date_str = meta.get('generated_at', '')[:10].replace('-', '')
    date_cn = meta.get('report_date', '')
    
    # 格式化日期
    weekday_map = {'Monday': '周一', 'Tuesday': '周二', 'Wednesday': '周三', 
                   'Thursday': '周四', 'Friday': '周五', 'Saturday': '周六', 'Sunday': '周日'}
    today = datetime.now()
    weekday = weekday_map.get(today.strftime('%A'), '')
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>股票热点早报 {date_cn} {weekday}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        
        /* Header */
        .header {{
            text-align: center;
            padding: 30px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            margin-bottom: 24px;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 8px;
            letter-spacing: 2px;
        }}
        .header .meta {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        /* Cards */
        .card {{
            background: rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .card h2 {{
            font-size: 18px;
            margin-bottom: 16px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .card h2 .icon {{ font-size: 20px; }}
        
        /* Market Index */
        .index-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 12px;
        }}
        .index-item {{
            background: rgba(255, 255, 255, 0.05);
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }}
        .index-item .name {{ font-size: 12px; color: #aaa; margin-bottom: 4px; }}
        .index-item .price {{ font-size: 20px; font-weight: bold; }}
        .index-item .change {{ font-size: 14px; }}
        .red {{ color: #ff4757; }}
        .green {{ color: #2ed573; }}
        
        /* Summary */
        .summary-card {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
            border-left: 4px solid #667eea;
        }}
        .summary-title {{ font-size: 20px; font-weight: bold; margin-bottom: 8px; }}
        .summary-desc {{ color: #ccc; font-size: 14px; }}
        
        /* Sectors */
        .sector-list {{}}
        .sector-item {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 12px;
        }}
        .sector-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        .sector-name {{
            font-size: 18px;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .sector-rank {{
            background: #667eea;
            color: #fff;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
        }}
        .sector-change {{
            font-size: 24px;
            font-weight: bold;
        }}
        .sector-meta {{
            display: flex;
            gap: 20px;
            font-size: 14px;
            color: #aaa;
            margin-bottom: 12px;
        }}
        .sector-driver {{
            background: rgba(46, 213, 115, 0.2);
            color: #2ed573;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 14px;
            margin-bottom: 12px;
        }}
        .sector-driver.warning {{
            background: rgba(255, 107, 107, 0.2);
            color: #ff6b6b;
        }}
        .risk-tag {{
            background: rgba(255, 107, 107, 0.3);
            color: #ff6b6b;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
        }}
        
        /* News */
        .news-list {{}}
        .news-item {{
            padding: 12px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            display: flex;
            gap: 12px;
        }}
        .news-item:last-child {{ border-bottom: none; }}
        .news-time {{
            color: #666;
            font-size: 12px;
            min-width: 60px;
        }}
        .news-content {{ flex: 1; }}
        .news-title {{ font-size: 14px; margin-bottom: 4px; }}
        .news-source {{ font-size: 12px; color: #888; }}
        
        /* Money Flow */
        .money-flow {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }}
        .flow-section h3 {{
            font-size: 14px;
            color: #aaa;
            margin-bottom: 12px;
        }}
        .flow-item {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            font-size: 14px;
        }}
        
        /* Sentiment */
        .sentiment-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 12px;
        }}
        .sentiment-item {{
            background: rgba(255, 255, 255, 0.05);
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }}
        .sentiment-item .value {{ font-size: 24px; font-weight: bold; }}
        .sentiment-item .label {{ font-size: 12px; color: #aaa; margin-top: 4px; }}
        
        /* Outlook */
        .outlook-card {{
            background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(255, 142, 83, 0.2) 100%);
        }}
        .outlook-tips {{
            font-size: 16px;
            line-height: 1.6;
            padding: 12px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
        }}
        .hotspot-list, .risk-list {{
            margin-top: 16px;
        }}
        .hotspot-item, .risk-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 6px;
            margin-bottom: 8px;
        }}
        
        /* External */
        .external-section {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 12px;
        }}
        
        @media (max-width: 600px) {{
            .money-flow, .external-section {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>📈 股票热点早报</h1>
            <div class="meta">{date_cn} {weekday}</div>
        </div>
        
        <!-- 核心摘要 -->
        <div class="card summary-card">
            <h2><span class="icon">🎯</span> 核心摘要</h2>
            <div class="summary-title">{summary.get('main_line', 'N/A')}</div>
            <div class="summary-desc">{summary.get('description', '')}</div>
            <div style="margin-top: 12px; display: flex; gap: 12px; flex-wrap: wrap;">
                <span>💰 资金方向: {summary.get('funding_direction', 'N/A')}</span>
                <span>🔥 热点: {', '.join(summary.get('hot_sectors', []))}</span>
            </div>
        </div>
        
        <!-- 大盘指数 -->
        <div class="card">
            <h2><span class="icon">📊</span> 大盘指数</h2>
            <div class="index-grid">'''
    
    # 添加指数
    for key, idx in market.items():
        name = idx.get('name', key)
        close = idx.get('close', 0)
        change = idx.get('change', 0)
        color_class = 'red' if change > 0 else 'green'
        arrow = '↑' if change > 0 else '↓'
        html += f'''
                <div class="index-item">
                    <div class="name">{name}</div>
                    <div class="price">{close:.2f}</div>
                    <div class="change {color_class}">{arrow} {change:+.2f}%</div>
                </div>'''
    
    html += '''
            </div>
        </div>
        
        <!-- 活跃板块详解 -->
        <div class="card">
            <h2><span class="icon">🔥</span> 活跃板块详解</h2>
            <div class="sector-list">'''
    
    # 添加板块
    for sector in sectors[:5]:
        rank = sector.get('rank', 0)
        name = sector.get('name', '')
        price_change = sector.get('price_change', 0)
        turnover = sector.get('turnover', '0')
        leader = sector.get('leader_stock', '')
        leader_change = sector.get('leader_change', '0')
        driver = sector.get('driver', '待确认')
        risk_level = sector.get('risk_level', 'medium')
        
        color_class = 'red' if price_change > 0 else 'green'
        arrow = '↑' if price_change > 0 else '↓'
        driver_class = '' if risk_level == 'low' else 'warning'
        
        html += f'''
                <div class="sector-item">
                    <div class="sector-header">
                        <div class="sector-name">
                            <span class="sector-rank">TOP{rank}</span>
                            {name}
                        </div>
                        <div class="sector-change {color_class}">{arrow} {price_change:+.2f}%</div>
                    </div>
                    <div class="sector-meta">
                        <span>📈 领涨: {leader} ({leader_change})</span>
                        <span>💵 成交额: {turnover}</span>
                    </div>
                    <div class="sector-driver {driver_class}">
                        🚀 驱动逻辑: {driver if driver else '无明确驱动，需警惕风险'}
                    </div>
                    {'<div class="risk-tag">⚠️ 无明确驱动因素</div>' if risk_level == 'high' else ''}
                </div>'''
    
    html += '''
            </div>
        </div>
        
        <!-- 资金流向 -->
        <div class="card">
            <h2><span class="icon">💰</span> 资金风向</h2>
            <div class="money-flow">'''
    
    # 主力净流入
    inflow = money_flow.get('main_inflow', [])
    html += f'''
                <div class="flow-section">
                    <h3>⬆️ 主力净流入</h3>'''
    for item in inflow[:5]:
        html += f'''
                    <div class="flow-item">
                        <span>{item.get('name', '')}</span>
                        <span class="red">{item.get('fund_flow', '')}</span>
                    </div>'''
    html += '''
                </div>'''
    
    # 主力净流出
    outflow = money_flow.get('main_outflow', [])
    html += f'''
                <div class="flow-section">
                    <h3>⬇️ 主力净流出</h3>'''
    for item in outflow[:5]:
        html += f'''
                    <div class="flow-item">
                        <span>{item.get('name', '')}</span>
                        <span class="green">{item.get('fund_flow', '')}</span>
                    </div>'''
    html += '''
                </div>
            </div>
        </div>
        
        <!-- 市场情绪 -->
        <div class="card">
            <h2><span class="icon">😊</span> 市场情绪</h2>
            <div class="sentiment-grid">'''
    
    # 情绪指标
    sentiment_items = [
        ('hot_level', '情绪热度', sentiment.get('hot_level', 'N/A')),
        ('turnover_rate', '换手率', sentiment.get('turnover_rate', 'N/A')),
        ('涨停数量', '涨停', str(sentiment.get('涨停数量', 0))),
        ('跌停数量', '跌停', str(sentiment.get('跌停数量', 0))),
        ('上涨家数', '上涨', str(sentiment.get('上涨家数', 0))),
        ('下跌家数', '下跌', str(sentiment.get('下跌家数', 0))),
    ]
    for key, label, value in sentiment_items:
        html += f'''
                <div class="sentiment-item">
                    <div class="value">{value}</div>
                    <div class="label">{label}</div>
                </div>'''
    
    html += f'''
            </div>
            <p style="margin-top: 12px; color: #aaa; font-size: 14px;">{sentiment.get('情绪解读', '')}</p>
        </div>
        
        <!-- 政策与资讯 -->
        <div class="card">
            <h2><span class="icon">📰</span> 政策与资讯</h2>
            <div class="news-list">'''
    
    for item in news[:8]:
        title = item.get('title', '')
        source = item.get('source', '')
        time = item.get('time', '')
        html += f'''
                <div class="news-item">
                    <div class="news-time">{time[-5:]}</div>
                    <div class="news-content">
                        <div class="news-title">{title}</div>
                        <div class="news-source">{source}</div>
                    </div>
                </div>'''
    
    html += '''
            </div>
        </div>
        
        <!-- 外围市场 -->
        <div class="card">
            <h2><span class="icon">🌏</span> 外围市场</h2>
            <div class="external-section">
                <div>
                    <h3>🇺🇸 美股隔夜</h3>'''
    
    us = external.get('us', {})
    for idx in us.get('indices', [])[:3]:
        html += f'''
                    <div class="flow-item">
                        <span>{idx.get('name', '')}</span>
                        <span>{idx.get('change', '')}</span>
                    </div>'''
    
    html += '''
                </div>
                <div>
                    <h3>🇭🇰 港股</h3>'''
    
    hk = external.get('hk', {})
    for idx in hk.get('indices', [])[:3]:
        html += f'''
                    <div class="flow-item">
                        <span>{idx.get('name', '')}</span>
                        <span>{idx.get('change', '')}</span>
                    </div>'''
    
    html += '''
                </div>
            </div>
        </div>
        
        <!-- 今日前瞻 -->
        <div class="card outlook-card">
            <h2><span class="icon">🔮</span> 今日前瞻</h2>
            <div class="outlook-tips">
                💡 {outlook.get('trading_tips', '暂无建议')}
            </div>'''
    
    hotspots = outlook.get('possible_hotspots', [])
    if hotspots:
        html += '''
            <div class="hotspot-list">
                <h3>🔥 潜在热点</h3>'''
        for h in hotspots:
            html += f'''
                <div class="hotspot-item">
                    <span>⭐</span>
                    <span>{h.get('name', '')}</span>
                    <span style="color: #888;">({h.get('source', '')})</span>
                </div>'''
        html += '''
            </div>'''
    
    risks = outlook.get('risk_alerts', [])
    if risks:
        html += '''
            <div class="risk-list">
                <h3>⚠️ 风险提示</h3>'''
        for r in risks:
            html += f'''
                <div class="risk-item">
                    <span>⚠️</span>
                    <span>{r.get('sector', '')}</span>
                    <span style="color: #888;">({r.get('reason', '')})</span>
                </div>'''
        html += '''
            </div>'''
    
    html += f'''
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>📊 数据来源: AkShare | 🤖 由AI股票早报系统 v2.0 自动生成</p>
            <p>生成时间: {meta.get('generated_at', '')}</p>
        </div>
    </div>
</body>
</html>'''
    
    return html


def main():
    """主函数"""
    print("=" * 60)
    print("🚀 股票热点早报生成器 (专业版 v2.0)")
    print("=" * 60)
    
    # 1. 获取专业级数据
    print("\n正在获取专业级早报数据...")
    analyzer = ReportAnalyzer()
    report_data = analyzer.compile_daily_report()
    
    # 2. 生成HTML
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    date_cn = now.strftime('%Y年%m月%d日')
    
    # 生成首页
    html = generate_professional_html(report_data)
    
    # 保存首页
    index_path = os.path.join(SITE_DIR, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ 生成首页: {index_path}")
    
    # 保存日报
    daily_path = os.path.join(DAILY_DIR, f'{date_str}.html')
    with open(daily_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ 生成日报: {daily_path}")
    
    # 保存JSON数据（已在analyzer中保存）
    data_path = os.path.join(DATA_DIR, f'{date_str}.json')
    print(f"✅ 保存数据: {data_path}")
    
    # 3. 更新归档
    update_archive(date_str, date_cn)
    
    print("\n" + "=" * 60)
    print("✅ 专业版早报生成完成！")
    print("=" * 60)


def update_archive(date_str: str, date_cn: str):
    """更新归档页面"""
    # 简单更新index.html的归档链接
    # 实际可以创建一个archive.html
    pass


if __name__ == "__main__":
    main()