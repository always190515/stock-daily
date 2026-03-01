# 🚀 股票热点日报网站 - 部署指南

## ✅ 已完成

- [x] 网站代码生成（HTML/CSS/JS）
- [x] Git 仓库初始化
- [x] 首次提交完成
- [x] 生成今日日报（2026-03-01）

## 📋 下一步：部署到 Vercel

### 方案 A：通过 GitHub 部署（推荐）

#### 1️⃣ 创建 GitHub 仓库

```bash
# 在 GitHub 网站上操作：
# 1. 登录 https://github.com
# 2. 点击右上角 "+" -> "New repository"
# 3. 仓库名：stock-daily
# 4. 选择 Public 或 Private
# 5. 点击 "Create repository"
```

#### 2️⃣ 推送到 GitHub

```bash
cd /app/working/stock_daily_site

# 替换为你的 GitHub 用户名
git remote add origin https://github.com/YOUR_USERNAME/stock-daily.git

# 推送
git branch -M main
git push -u origin main
```

#### 3️⃣ 在 Vercel 部署

```bash
# 访问 https://vercel.com
# 1. 用 GitHub 账号登录
# 2. 点击 "New Project"
# 3. 找到 "stock-daily" 仓库
# 4. 点击 "Import"
# 5. 保持默认设置，点击 "Deploy"
# 6. 等待部署完成（约 30 秒）
```

部署完成后，你会获得一个域名：
```
https://stock-daily-xxxx.vercel.app
```

### 方案 B：使用 Vercel CLI 直接部署

```bash
# 安装 Vercel CLI
npm install -g vercel

# 登录 Vercel
vercel login

# 部署
cd /app/working/stock_daily_site
vercel --prod
```

## ⏰ 配置定时更新

### 更新 cron 任务

删除旧的 PDF 任务，创建新的网站更新任务：

```bash
# 删除旧任务（如果存在）
copaw cron list  # 查看任务 ID
copaw cron delete TASK_ID

# 创建新任务（北京时间 8:15，周一至周五）
copaw cron create --type text --name "股票日报网站更新" --cron "15 0 * * 1-5" --channel console --target-user default --target-session 1772357503087 --text "cd /app/working/stock_daily_site && python3 generate.py && cd /app/working/stock_daily_site && git add . && git commit -m 'Daily update: \$(date +\%Y\%m\%d)' && git push"
```

### 自动推送流程

每天早上 8:15 自动执行：
1. ✅ 运行 `generate.py` 生成今日日报
2. ✅ Git add + commit 提交更改
3. ✅ Git push 推送到 GitHub
4. ✅ Vercel 自动检测更改并重新部署（约 30 秒）
5. ✅ 网站自动更新

## 📱 飞书推送配置

创建飞书推送脚本：

```python
# /app/working/stock_daily_site/send_feishu.py
import requests
import json

FEISHU_APP_ID = 'cli_a929700eb1789bd2'
FEISHU_APP_SECRET = 'GVgubHX4lb7j6x5ojyMP0ejvhheT6Pcz'
FEISHU_USER_ID = 'ou_4c219a0a98df4db783e4bc0cadc2ecb9'
SITE_URL = 'https://YOUR-SITE.vercel.app'  # 替换为你的 Vercel 域名

def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET})
    return resp.json().get('tenant_access_token')

def send_message():
    token = get_token()
    from datetime import datetime
    date_cn = datetime.now().strftime('%Y年%m月%d日')
    
    text = f"""📈 股票热点日报 - {date_cn}

🔗 查看今日报告：{SITE_URL}

内容包括：
• 大盘指数概况（上证/深证/创业板）
• 热点板块 TOP8
• 重要财经新闻 TOP12
• 历史归档可回溯

点击链接查看完整报告 👆"""
    
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {
        "receive_id": FEISHU_USER_ID,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }
    
    resp = requests.post(url, headers=headers, json=payload)
    print(resp.json())

if __name__ == "__main__":
    send_message()
```

## 🎨 网站预览

访问生成的本地文件预览：
```bash
# 在浏览器打开
open /app/working/stock_daily_site/index.html
```

## 📊 网站结构

```
https://YOUR-SITE.vercel.app/
├── /                    # 首页（今日日报）
├── /archive.html        # 历史归档（最近 30 天）
├── /daily/
│   ├── 20260301.html   # 2026-03-01 日报
│   ├── 20260228.html   # 2026-02-28 日报
│   └── ...
├── /data/
│   ├── 20260301.json   # 原始数据
│   └── ...
├── /css/style.css       # 样式
└── /js/main.js          # 交互
```

## 🔧 自定义配置

### 修改样式

编辑 `/app/working/stock_daily_site/css/style.css`

### 修改数据源

编辑 `/app/working/stock_daily_site/generate.py` 中的 `get_stock_data()` 函数

### 修改更新频率

修改 cron 表达式：
- 每天 8:15：`15 0 * * 1-5`（周一至周五）
- 每天 8:15（含周末）：`15 0 * * *`
- 交易日 15:30：`30 7 * * 1-5`

## 📝 注意事项

1. **GitHub 仓库名**：确保与 Vercel 项目名称一致
2. **Vercel 域名**：部署后记得替换飞书推送脚本中的 `SITE_URL`
3. **Git 凭证**：首次 push 可能需要输入 GitHub 账号密码或使用 SSH
4. **数据准确性**：目前使用备用数据，建议接入真实 API

## 🎉 完成！

部署成功后，你会：
- ✅ 拥有一个永久免费的静态网站
- ✅ 每天早上 8:15 自动更新
- ✅ 在飞书收到推送链接
- ✅ 可以随时查看历史日报

有任何问题随时问我！
