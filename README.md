# 股票热点日报网站

每日自动生成股票热点日报静态网站，托管在 Vercel。

## 📁 目录结构

```
stock_daily_site/
├── index.html          # 首页（今日日报）
├── archive.html        # 历史归档页
├── daily/              # 每日日报
│   └── YYYYMMDD.html
├── data/               # 数据 JSON
│   └── YYYYMMDD.json
├── css/
│   └── style.css       # 样式文件
├── js/
│   └── main.js         # JavaScript
└── generate.py         # 生成脚本
```

## 🚀 部署到 Vercel

### 方法 1：GitHub + Vercel（推荐）

1. **创建 GitHub 仓库**
   ```bash
   cd /app/working/stock_daily_site
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/stock-daily.git
   git push -u origin main
   ```

2. **在 Vercel 部署**
   - 访问 https://vercel.com
   - 登录 GitHub
   - 点击 "New Project"
   - 选择 `stock-daily` 仓库
   - 点击 "Deploy"
   - 完成！获得域名如：`https://stock-daily.vercel.app`

### 方法 2：Vercel CLI

```bash
# 安装 Vercel CLI
npm i -g vercel

# 部署
cd /app/working/stock_daily_site
vercel --prod
```

## ⏰ 定时更新

配置 cron 任务，每天早上 8:15 运行：

```bash
copaw cron create --type text --name "股票日报网站" --cron "15 0 * * 1-5" --channel console --target-user default --target-session YOUR_SESSION --text "cd /app/working/stock_daily_site && python3 generate.py && git add . && git commit -m 'Daily update' && git push"
```

## 📱 飞书推送

生成网站后，通过飞书发送链接：

```
📈 股票热点日报 - 2026 年 03 月 01 日

🔗 查看今日报告：https://YOUR-SITE.vercel.app

内容包括：
• 大盘指数概况
• 热点板块 TOP8
• 重要财经新闻 TOP12
• 历史归档
```

## 🎨 特点

- ✅ 响应式设计，手机友好
- ✅ 渐变背景，现代化 UI
- ✅ 红绿涨跌颜色标识
- ✅ 历史归档可回溯
- ✅ 静态网站，加载快
- ✅ 免费托管（Vercel）

## 📊 数据源

- 板块数据：东方财富
- 大盘指数：AkShare
- 财经新闻：备用数据（可接入真实 API）

## 📝 许可证

MIT
