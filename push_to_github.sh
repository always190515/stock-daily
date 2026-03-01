#!/bin/bash
# 股票日报网站 - GitHub 推送脚本
# 使用方法：./push_to_github.sh

set -e

echo "=========================================="
echo "🚀 推送股票日报网站到 GitHub"
echo "=========================================="

cd /app/working/stock_daily_site

# 检查远程仓库
echo ""
echo "📋 当前远程仓库:"
git remote -v

# 推送代码
echo ""
echo "📤 正在推送到 GitHub..."
echo "💡 提示：首次推送需要输入 GitHub 用户名和密码（或 Personal Access Token）"
echo ""

git branch -M main
git push -u origin main

echo ""
echo "=========================================="
echo "✅ 推送成功！"
echo "=========================================="
echo ""
echo "📱 下一步："
echo "1. 访问 https://vercel.com"
echo "2. 用 GitHub 账号登录"
echo "3. 点击 'New Project'"
echo "4. 选择 'stock-daily' 仓库"
echo "5. 点击 'Deploy'"
echo ""
echo "🎉 完成！"
