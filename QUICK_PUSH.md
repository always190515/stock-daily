# 🚀 快速推送指南

## ⚡ 最快方式（3 步完成）

### 第 1 步：获取 GitHub Token

1. 访问：https://github.com/settings/tokens/new
2. Token 名称：`stock-daily-deploy`
3. 过期时间：选择 `90 days` 或 `No expiration`
4. 权限：勾选 **`repo`** (Full control of private repositories)
5. 点击 **Generate token**
6. **复制 token**（以 `ghp_` 开头，只显示一次！）

### 第 2 步：运行推送命令

```bash
cd /app/working/stock_daily_site

# 替换 YOUR_TOKEN 为刚才复制的 token
git remote set-url origin https://always190515:YOUR_TOKEN@github.com/always190515/stock-daily.git

# 推送
git branch -M main
git push -u origin main
```

### 第 3 步：验证

访问 https://github.com/always190515/stock-daily
应该能看到所有文件已上传 ✅

---

## 📱 然后部署到 Vercel

1. 访问 https://vercel.com
2. 用 GitHub 登录
3. 点击 **New Project**
4. 找到 `stock-daily` 仓库，点击 **Import**
5. 点击 **Deploy**
6. 等待 30 秒，完成！🎉

你会获得一个域名：`https://stock-daily.vercel.app`

---

## 🔧 配置自动更新

部署成功后，运行以下命令配置每天自动更新：

```bash
copaw cron create --type text --name "股票日报网站" --cron "15 0 * * 1-5" --channel console --target-user default --target-session 1772357503087 --text "cd /app/working/stock_daily_site && python3 generate.py && git add . && git commit -m 'Daily update' && git push"
```

---

## ❓ 需要帮助？

如果遇到问题：
1. 检查 token 是否正确（以 `ghp_` 开头）
2. 确保 token 有 `repo` 权限
3. 检查网络连接
4. 查看错误信息

把错误信息发给我，我会帮你解决！
