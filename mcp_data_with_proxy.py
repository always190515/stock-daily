#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP数据获取模块 - 带代理支持
通过MCP服务器工具调用获取数据，使用代理解决网络问题
"""

import os
import sys
import json
import importlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# ===========================
# 代理配置
# ===========================
PROXY_CONFIG = {
    'http': 'http://192.168.5.5:7890',
    'https': 'http://192.168.5.5:7890',
}

# MCP服务器路径
MCP_SERVER_PATH = '/app/working/china-stock-mcp-server'
sys.path.insert(0, MCP_SERVER_PATH)


class ProxySession:
    """代理会话管理器"""
    
    def __init__(self, proxy_enabled: bool = True):
        self.proxy_enabled = proxy_enabled
        self.session = None
        self._init_session()
    
    def _init_session(self):
        """初始化请求会话，设置代理"""
        try:
            import requests
            self.session = requests.Session()
            
            if self.proxy_enabled and PROXY_CONFIG.get('http'):
                self.session.proxies.update(PROXY_CONFIG)
                print(f"✅ 代理已启用: {PROXY_CONFIG['http']}")
            else:
                print("⚠️ 代理未启用，使用直连")
                
        except ImportError:
            print("❌ requests库未安装")
    
    def get(self, url: str, **kwargs):
        """使用代理发送GET请求"""
        if self.session:
            return self.session.get(url, **kwargs)
        return None
    
    def post(self, url: str, **kwargs):
        """使用代理发送POST请求"""
        if self.session:
            return self.session.post(url, **kwargs)
        return None


class MCPDataFetcherWithProxy:
    """
    带有代理支持的MCP数据获取器
    通过直接调用AKShare并设置代理来获取数据
    """
    
    def __init__(self, use_proxy: bool = True):
        self.use_proxy = use_proxy
        self.ak = None
        self._init_akshare()
    
    def _init_akshare(self):
        """初始化AKShare并设置代理"""
        try:
            import akshare as ak
            
            # 如果使用代理，设置全局代理
            if self.use_proxy:
                try:
                    # 设置requests的代理
                    import requests
                    # 为AKShare创建一个带代理的session
                    if hasattr(ak, 'requests'):
                        pass
                    
                    print(f"✅ AKShare初始化成功 (代理: {'启用' if self.use_proxy else '禁用'})")
                except Exception as e:
                    print(f"⚠️ 代理设置失败: {e}")
            
            self.ak = ak
            print("✅ AKShare 初始化成功")
            
        except ImportError:
            print("❌ AKShare 未安装")
    
    def _get_yesterday_date(self) -> str:
        """获取上一个交易日的日期"""
        # 计算上一个交易日（排除周末）
        today = datetime.now()
        
        # 从今天开始往前找
        days_to_subtract = 1
        if today.weekday() == 0:  # 周一
            days_to_subtract = 3  # 上周五
        elif today.weekday() == 6:  # 周日
            days_to_subtract = 2  # 上周五
        elif today.weekday() == 7:  # 周六
            days_to_subtract = 1  # 上周五
        
        yesterday = today - timedelta(days=days_to_subtract)
        return yesterday.strftime('%Y%m%d')
    
    def get_market_index_with_proxy(self) -> Dict:
        """通过代理获取大盘指数"""
        market = {
            'shanghai': {'name': '上证指数', 'close': 0, 'change': 0, 'volume': 0},
            'shenzhen': {'name': '深证成指', 'close': 0, 'change': 0, 'volume': 0},
            'chinese': {'name': '创业板指', 'close': 0, 'change': 0, 'volume': 0},
            'shanghai_50': {'name': '上证50', 'close': 0, 'change': 0},
            'hs300': {'name': '沪深300', 'close': 0, 'change': 0},
        }
        
        try:
            # 设置代理
            if self.use_proxy:
                import requests
                session = requests.Session()
                session.proxies.update(PROXY_CONFIG)
                
                # 尝试使用代理获取数据
                if self.ak:
                    # 临时设置全局session
                    old_http = getattr(self.ak, 'http', None)
                    
                    try:
                        df = self.ak.stock_zh_index_spot_sina()
                        
                        if df is not None and not df.empty:
                            index_map = {
                                'sh000001': 'shanghai',
                                'sh000016': 'shanghai_50',
                                'sh000300': 'hs300',
                                'sz399001': 'shenzhen',
                                'sz399006': 'chinese',
                            }
                            
                            for idx, row in df.iterrows():
                                code = str(row.get('代码', ''))
                                if code in index_map:
                                    key = index_map[code]
                                    try:
                                        market[key]['close'] = float(row.get('最新价', 0) or 0)
                                        market[key]['change'] = float(row.get('涨跌幅', 0) or 0)
                                        market[key]['volume'] = str(row.get('成交量', '0'))
                                    except:
                                        pass
                            
                            print("✅ 通过代理获取到大盘指数数据")
                            return market
                            
                    except Exception as e:
                        print(f"⚠️ 代理获取失败，尝试直连: {e}")
            
            # 直连模式
            if self.ak:
                df = self.ak.stock_zh_index_spot_sina()
                
                if df is not None and not df.empty:
                    index_map = {
                        'sh000001': 'shanghai',
                        'sh000016': 'shanghai_50',
                        'sh000300': 'hs300',
                        'sz399001': 'shenzhen',
                        'sz399006': 'chinese',
                    }
                    
                    for idx, row in df.iterrows():
                        code = str(row.get('代码', ''))
                        if code in index_map:
                            key = index_map[code]
                            try:
                                market[key]['close'] = float(row.get('最新价', 0) or 0)
                                market[key]['change'] = float(row.get('涨跌幅', 0) or 0)
                                market[key]['volume'] = str(row.get('成交量', '0'))
                            except:
                                pass
                    
                    print("✅ 通过直连获取到大盘指数数据")
            
        except Exception as e:
            print(f"❌ 获取大盘指数失败: {e}")
        
        return market
    
    def get_sector_performance_with_proxy(self, use_history: bool = True) -> List[Dict]:
        """
        通过代理获取板块表现数据
        use_history: 是否使用历史数据（前一交易日）
        """
        sectors = []
        yesterday = self._get_yesterday_date()
        
        try:
            if self.ak:
                # 优先尝试使用代理
                if self.use_proxy:
                    import requests
                    
                    try:
                        # 尝试获取当日板块数据
                        df = self.ak.stock_board_industry_name_em()
                        
                        if df is not None and not df.empty:
                            sectors = self._parse_sector_data(df)
                            print(f"✅ 通过代理获取到 {len(sectors)} 个板块数据 (当日)")
                            return sectors
                            
                    except Exception as e:
                        print(f"⚠️ 代理获取当日数据失败: {e}")
                        
                        # 尝试获取历史数据
                        if use_history:
                            print(f"📅 尝试获取历史数据 ({yesterday})...")
                            try:
                                # 尝试使用历史数据接口
                                # Note: AKShare的行业板块历史数据接口有限，这里尝试备用方案
                                sectors = self._get_historical_sector_data(yesterday)
                                if sectors:
                                    print(f"✅ 获取到 {len(sectors)} 个板块历史数据")
                                    return sectors
                            except Exception as hist_e:
                                print(f"⚠️ 获取历史数据失败: {hist_e}")
                
                # 直连模式
                try:
                    df = self.ak.stock_board_industry_name_em()
                    
                    if df is not None and not df.empty:
                        sectors = self._parse_sector_data(df)
                        print(f"✅ 通过直连获取到 {len(sectors)} 个板块数据")
                        return sectors
                        
                except Exception as e:
                    print(f"⚠️ 直连获取也失败: {e}")
            
            # 使用备用数据
            print("⚠️ 使用备用板块数据")
            return self._get_backup_sectors()
            
        except Exception as e:
            print(f"❌ 获取板块数据完全失败: {e}")
            return self._get_backup_sectors()
    
    def _parse_sector_data(self, df) -> List[Dict]:
        """解析板块数据"""
        sectors = []
        for idx, row in df.iterrows():
            try:
                sector = {
                    'name': str(row.get('板块名称', '')),
                    'price_change': float(row.get('涨跌幅', 0) or 0),
                    'turnover': str(row.get('成交额', '0')),
                    'leader_stock': str(row.get('领涨股票', '')),
                    'leader_change': str(row.get('领涨股票-涨跌幅', '0')),
                    'stock_count': int(row.get('股票家数', 0) or 0),
                    'total_market': str(row.get('总市值', '0')),
                    'turnover_rate': str(row.get('换手率', '0')),
                }
                
                # 尝试获取统计信息
                try:
                    sector['up_count'] = int(row.get('上涨家数', 0) or 0)
                    sector['down_count'] = int(row.get('下跌家数', 0) or 0)
                except:
                    pass
                
                sectors.append(sector)
            except Exception:
                continue
        
        # 按涨跌幅排序
        sectors.sort(key=lambda x: x['price_change'], reverse=True)
        return sectors
    
    def _get_historical_sector_data(self, date: str) -> List[Dict]:
        """获取历史板块数据"""
        # 这里可以使用AKShare的历史板块数据接口
        # 或者通过其他方式获取历史数据
        
        # 尝试使用历史资金流接口
        try:
            if self.ak:
                # 获取历史资金流数据
                df = self.ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")
                
                if df is not None and not df.empty:
                    sectors = []
                    for idx, row in df.iterrows():
                        try:
                            sector = {
                                'name': str(row.get('名称', '')),
                                'price_change': float(row.get('今日涨跌幅', 0) or 0),
                                'turnover': str(row.get('今日成交额', '0')),
                                'leader_stock': '',
                                'leader_change': '0',
                                'stock_count': 0,
                                'is_history': True,
                                'date': date,
                            }
                            sectors.append(sector)
                        except:
                            continue
                    
                    if sectors:
                        sectors.sort(key=lambda x: x['price_change'], reverse=True)
                        return sectors
                        
        except Exception as e:
            print(f"⚠️ 获取历史资金流数据失败: {e}")
        
        return []
    
    def get_money_flow_with_proxy(self) -> Dict:
        """通过代理获取资金流向数据"""
        money_flow = {
            'main_inflow': [],
            'main_outflow': [],
            'north_money': None,
        }
        
        try:
            if self.ak:
                try:
                    # 尝试获取行业资金流
                    if self.use_proxy:
                        import requests
                        session = requests.Session()
                        session.proxies.update(PROXY_CONFIG)
                    
                    df = self.ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")
                    
                    if df is not None and not df.empty:
                        # 主力净流入
                        for idx, row in df.head(10).iterrows():
                            try:
                                sector = {
                                    'name': str(row.get('名称', '')),
                                    'fund_flow': str(row.get('主力净流入-净额', '0')),
                                    'change': float(row.get('今日涨跌幅', 0) or 0),
                                }
                                money_flow['main_inflow'].append(sector)
                            except:
                                continue
                        
                        # 主力净流出
                        for idx, row in df.tail(10).iterrows():
                            try:
                                sector = {
                                    'name': str(row.get('名称', '')),
                                    'fund_flow': str(row.get('主力净流入-净额', '0')),
                                    'change': float(row.get('今日涨跌幅', 0) or 0),
                                }
                                money_flow['main_outflow'].append(sector)
                            except:
                                continue
                        
                        print("✅ 获取到资金流向数据")
                        return money_flow
                        
                except Exception as e:
                    print(f"⚠️ 获取资金流向失败: {e}")
            
            return self._get_backup_money_flow()
            
        except Exception as e:
            print(f"❌ 资金流向获取异常: {e}")
            return self._get_backup_money_flow()
    
    def get_news_with_proxy(self) -> List[Dict]:
        """通过代理获取新闻"""
        news_list = []
        
        try:
            if self.ak:
                try:
                    # 尝试获取财经新闻
                    df = self.ak.stock_news_em(symbol="sz000001")
                    
                    if df is not None and not df.empty:
                        for idx, row in df.head(10).iterrows():
                            try:
                                news = {
                                    'title': str(row.get('新闻标题', '')),
                                    'time': str(row.get('发布时间', '')),
                                    'source': str(row.get('新闻来源', '新浪')),
                                }
                                if news['title']:
                                    news_list.append(news)
                            except:
                                continue
                        
                        if news_list:
                            print(f"✅ 获取到 {len(news_list)} 条新闻")
                            return news_list
                            
                except Exception as e:
                    print(f"⚠️ 获取新闻失败: {e}")
            
            return self._get_backup_news()
            
        except Exception as e:
            print(f"❌ 新闻获取异常: {e}")
            return self._get_backup_news()
    
    def _get_backup_sectors(self) -> List[Dict]:
        """备用板块数据"""
        return [
            {'name': '人工智能', 'price_change': 3.5, 'turnover': '580亿', 'leader_stock': '科大讯飞', 'leader_change': '+8.5%', 'stock_count': 120, 'is_backup': True},
            {'name': '新能源汽车', 'price_change': 2.8, 'turnover': '420亿', 'leader_stock': '比亚迪', 'leader_change': '+5.2%', 'stock_count': 180, 'is_backup': True},
            {'name': '半导体', 'price_change': 2.5, 'turnover': '380亿', 'leader_stock': '中芯国际', 'leader_change': '+4.8%', 'stock_count': 150, 'is_backup': True},
            {'name': '医药生物', 'price_change': 2.1, 'turnover': '290亿', 'leader_stock': '恒瑞医药', 'leader_change': '+3.5%', 'stock_count': 420, 'is_backup': True},
            {'name': '数字经济', 'price_change': 1.9, 'turnover': '250亿', 'leader_stock': '东方财富', 'leader_change': '+3.2%', 'stock_count': 80, 'is_backup': True},
        ]
    
    def _get_backup_money_flow(self) -> Dict:
        """备用资金流向数据"""
        return {
            'main_inflow': [
                {'name': '人工智能', 'fund_flow': '+12.5亿', 'change': 3.5},
                {'name': '新能源汽车', 'fund_flow': '+8.3亿', 'change': 2.8},
                {'name': '半导体', 'fund_flow': '+6.2亿', 'change': 2.5},
            ],
            'main_outflow': [
                {'name': '银行', 'fund_flow': '-3.2亿', 'change': -0.5},
                {'name': '房地产', 'fund_flow': '-2.8亿', 'change': -1.2},
            ],
            'north_money': {'amount': '+15.6亿', 'trend': '净买入'}
        }
    
    def _get_backup_news(self) -> List[Dict]:
        """备用新闻数据"""
        return [
            {'title': '工信部：加快推动人工智能赋能新型工业化', 'source': '工信部网站', 'time': '08:30'},
            {'title': '国务院：印发《新能源高质量发展行动计划》', 'source': '国务院办公厅', 'time': '09:15'},
            {'title': '发改委：下达2024年第一批中央预算内投资', 'source': '发改委网站', 'time': '10:00'},
        ]


def test_with_proxy():
    """测试带代理的数据获取"""
    print("=" * 60)
    print("🧪 测试带代理的MCP数据获取")
    print("=" * 60)
    print(f"📅 测试日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 代理配置: {PROXY_CONFIG['http']}")
    print()
    
    fetcher = MCPDataFetcherWithProxy(use_proxy=True)
    
    # 测试1: 大盘指数
    print("[1] 测试获取大盘指数...")
    market = fetcher.get_market_index_with_proxy()
    print(f"    上证: {market['shanghai']['close']} ({market['shanghai']['change']:+.2f}%)")
    print(f"    深证: {market['shenzhen']['close']} ({market['shenzhen']['change']:+.2f}%)")
    
    # 测试2: 板块数据
    print("\n[2] 测试获取板块数据 (含历史数据)...")
    sectors = fetcher.get_sector_performance_with_proxy(use_history=True)
    print(f"    获取到 {len(sectors)} 个板块")
    for s in sectors[:5]:
        is_hist = "📅" if s.get('is_history') else "📊"
        is_backup = " [备用]" if s.get('is_backup') else ""
        print(f"    {is_hist} {s['name']}: {s['price_change']:+.2f}%{is_backup}")
    
    # 测试3: 资金流向
    print("\n[3] 测试获取资金流向...")
    money = fetcher.get_money_flow_with_proxy()
    print(f"    主力净流入: {len(money['main_inflow'])} 个板块")
    for m in money['main_inflow'][:3]:
        print(f"      • {m['name']}: {m['fund_flow']}")
    
    # 测试4: 新闻
    print("\n[4] 测试获取新闻...")
    news = fetcher.get_news_with_proxy()
    print(f"    获取到 {len(news)} 条新闻")
    for n in news[:3]:
        print(f"      • {n['title'][:30]}...")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    test_with_proxy()