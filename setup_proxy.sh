#!/bin/bash
# 股票日报 - 配置代理并安装 Playwright

echo "=========================================="
echo "🔧 配置代理并安装 Playwright"
echo "=========================================="

# 请修改下面的代理地址为你的实际代理
# 常见格式：
#   http://192.168.1.100:7890
#   http://127.0.0.1:7890
#   socks5://192.168.1.100:1080

PROXY_URL="http://YOUR_PROXY_IP:YOUR_PROXY_PORT"

echo ""
echo "⚠️  请先修改脚本中的代理地址："
echo "   编辑：/app/working/stock_daily_site/setup_proxy.sh"
echo "   将 PROXY_URL 改为你的实际代理地址"
echo ""
echo "例如："
echo "   PROXY_URL=\"http://192.168.1.100:7890\""
echo ""
echo "修改完成后重新运行："
echo "   bash /app/working/stock_daily_site/setup_proxy.sh"
echo ""

# 如果你已经知道代理地址，取消下面的注释并修改
# export HTTP_PROXY="$PROXY_URL"
# export HTTPS_PROXY="$PROXY_URL"
# export http_proxy="$PROXY_URL"
# export https_proxy="$PROXY_URL"

# echo "✅ 代理配置完成："
# echo "   HTTP_PROXY=$HTTP_PROXY"
# echo "   HTTPS_PROXY=$HTTPS_PROXY"

# echo ""
# echo "📦 开始安装 Playwright Chromium..."
# playwright install chromium

# echo ""
# echo "✅ 安装完成！测试运行..."
# cd /app/working/stock_daily_site
# python3 generate_web_playwright.py

echo "=========================================="
