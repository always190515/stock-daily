# 🎉 股票热点日报网站 - 准备就绪！

## ✅ 已完成的工作

| 项目 | 状态 | 说明 |
|------|------|------|
| 网站代码 | ✅ | HTML/CSS/JS 完整 |
| 生成脚本 | ✅ | `generate.py` 自动生成 |
| Git 仓库 | ✅ | 已初始化并提交 |
| GitHub 远程 | ✅ | 已配置 `origin` |
| 推送脚本 | ✅ | 3 种推送方式可选 |
| 部署文档 | ✅ | 详细指南 |
| Vercel 配置 | ✅ | `vercel.json` 已配置 |

---

## 📤 推送到 GitHub（3 选 1）

### 方式 A：使用自动推送脚本（最简单）

```bash
# 1. 获取 GitHub Token
# 访问：https://github.com/settings/tokens/new
# Token 名称：stock-daily-deploy
# 权限：勾选 'repo'
# 点击 'Generate token'，复制 token（ghp_开头）

# 2. 运行推送脚本
cd /app/working/stock_daily_site
python3 auto_push.py ghp_xxxxxxxxxxxxxxxxxxxx

# 3. 完成！访问 https://github.com/always190515/stock-daily 查看
```

### 方式 B：手动推送

```bash
cd /app/working/stock_daily_site

# 替换 YOUR_TOKEN 为你的 GitHub Token
git remote set-url origin https://always190515:YOUR_TOKEN@github.com/always190515/stock-daily.git

# 推送
git push -u origin main
```

### 方式 C：使用 shell 脚本

```bash
cd /app/working/stock_daily_site
chmod +x push_to_github.sh
./push_to_github.sh
# 按提示输入用户名和 token
```

---

## 🌐 部署到 Vercel

推送成功后：

1. **访问** https://vercel.com
2. **登录** GitHub 账号
3. **点击** "New Project"
4. **选择** `stock-daily` 仓库
5. **点击** "Deploy"
6. **等待** 30 秒

完成！获得域名：`https://stock-daily.vercel.app`

---

## ⏰ 配置自动更新

部署成功后，配置每天自动更新：

```bash
# 删除旧的 PDF 任务（如果有）
copaw cron list
copaw cron delete 旧任务 ID

# 创建新的网站更新任务
copaw cron create --type text --name "股票日报网站更新" --cron "15 0 * * 1-5" --channel console --target-user default --target-session 1772357503087 --text "cd /app/working/stock_daily_site && python3 generate.py && git add . && git commit -m 'Daily update' && git push"
```

---

## 📱 飞书推送配置

网站更新后，发送飞书消息：

```bash
# 创建飞书推送脚本
cat > /app/working/stock_daily_site/send_link.py << 'EOF'
import requests, json
from datetime import datetime

FEISHU_APP_ID = 'cli_a929700eb1789bd2'
FEISHU_APP_SECRET = 'GVgubHX4lb7j6x5ojyMP0ejvhheT6Pcz'
FEISHU_USER_ID = 'ou_4c219a0a98df4db783e4bc0cadc2ecb9'
SITE_URL = 'https://stock-daily.vercel.app'  # 替换为你的 Vercel 域名

def get_token():
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    )
    return resp.json().get('tenant_access_token')

def send():
    token = get_token()
    date_cn = datetime.now().strftime('%Y年%m月%d日')
    text = f"""📈 股票热点日报 - {date_cn}

🔗 查看今日报告：{SITE_URL}

内容包括：
• 大盘指数概况
• 热点板块 TOP8
• 重要财经新闻 TOP12
• 历史归档

点击链接查看 👆"""
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {
        "receive_id": FEISHU_USER_ID,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }
    
    resp = requests.post(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        headers=headers, json=payload
    )
    print(resp.json())

if __name__ == "__main__":
    send()
EOF

# 测试发送
python3 /app/working/stock_daily_site/send_link.py
```

---

## 📊 网站结构

```
https://stock-daily.vercel.app/
├── /                    # 首页（今日日报）
├── /archive.html        # 历史归档（30 天）
├── /daily/
│   ├── 20260301.html   # 每日日报
│   └── ...
├── /data/
│   ├── 20260301.json   # 原始数据
│   └── ...
├── /css/style.css       # 样式
└── /js/main.js          # 交互
```

---

## 🎨 网站特点

- ✅ **响应式设计**：手机/平板/电脑完美适配
- ✅ **渐变背景**：紫色渐变，现代化 UI
- ✅ **涨跌颜色**：红色上涨，绿色下跌
- ✅ **历史归档**：可查看任意历史日报
- ✅ **快速加载**：静态 HTML，秒开
- ✅ **免费托管**：Vercel 永久免费
- ✅ **自动更新**：每天早上 8:15 自动更新

---

## 🔗 重要链接

| 用途 | 链接 |
|------|------|
| GitHub 仓库 | https://github.com/always190515/stock-daily |
| Vercel 部署 | https://vercel.com |
| 获取 Token | https://github.com/settings/tokens/new |
| Vercel 文档 | https://vercel.com/docs |

---

## 📝 下一步行动清单

- [ ] **获取 GitHub Token**（5 分钟）
  - 访问 https://github.com/settings/tokens/new
  - 创建 token，权限选 `repo`
  
- [ ] **推送代码到 GitHub**（2 分钟）
  - 运行 `python3 auto_push.py ghp_xxx`
  - 或手动推送
  
- [ ] **部署到 Vercel**（2 分钟）
  - 访问 vercel.com
  - Import 仓库
  - Deploy
  
- [ ] **配置自动更新**（1 分钟）
  - 运行 cron 创建命令
  
- [ ] **测试飞书推送**（1 分钟）
  - 运行 send_link.py
  - 检查飞书是否收到

---

## 🎯 总结

你现在拥有：
- ✅ 一个完整的股票日报网站
- ✅ 自动化生成和部署流程
- ✅ 免费永久托管（Vercel）
- ✅ 每天早上 8:15 自动更新
- ✅ 飞书推送通知
- ✅ 完整历史归档

**总耗时**：约 10-15 分钟完成所有配置

**开始行动**：先获取 GitHub Token，然后运行 `python3 auto_push.py YOUR_TOKEN`

有任何问题随时问我！🚀
