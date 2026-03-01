# 📤 GitHub 推送指南

由于需要 GitHub 认证，请选择以下任一方式推送代码：

## 方式 1：使用推送脚本（推荐）

```bash
cd /app/working/stock_daily_site
chmod +x push_to_github.sh
./push_to_github.sh
```

首次推送会提示输入：
- **Username**: `always190515`
- **Password**: 你的 GitHub Personal Access Token

### 如何获取 Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选权限：`repo` (Full control of private repositories)
4. 点击 "Generate token"
5. **复制 token**（只显示一次，妥善保存）
6. 在推送时使用此 token 作为密码

## 方式 2：手动命令推送

```bash
cd /app/working/stock_daily_site

# 设置 Git 用户信息（如果之前没设置）
git config --global user.email "your-email@example.com"
git config --global user.name "always190515"

# 推送
git branch -M main
git push -u origin main
```

输入用户名和密码（token）：
- Username: `always190515`
- Password: `[你的 Personal Access Token]`

## 方式 3：使用 GitHub Desktop（图形界面）

1. 下载 https://desktop.github.com
2. 登录 GitHub 账号
3. File -> Add Local Repository -> 选择 `/app/working/stock_daily_site`
4. 点击 "Push origin"

## 方式 4：SSH 方式（如果你配置了 SSH key）

```bash
cd /app/working/stock_daily_site

# 修改远程仓库为 SSH 方式
git remote set-url origin git@github.com:always190515/stock-daily.git

# 推送
git push -u origin main
```

---

## ✅ 推送成功后

1. **验证推送**：
   访问 https://github.com/always190515/stock-daily
   应该能看到所有文件

2. **部署到 Vercel**：
   - 访问 https://vercel.com
   - 用 GitHub 登录
   - New Project -> 选择 `stock-daily`
   - Deploy

3. **配置自动更新**：
   推送成功后，告诉我，我会帮你配置 cron 任务

---

## 🔐 为什么需要 Token？

GitHub 从 2021 年起不再支持密码推送，必须使用：
- Personal Access Token（推荐）
- SSH Key
- GitHub CLI

最快速的方式是使用 Personal Access Token，5 分钟即可完成。
