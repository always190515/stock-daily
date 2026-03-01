# 🔧 配置代理并安装 Playwright 完整指南

## 📋 步骤总览

1. 获取你的局域网代理地址
2. 配置代理到脚本中
3. 安装 Playwright Chromium
4. 测试运行
5. 更新定时任务

---

## 1️⃣ 获取局域网代理地址

### 常见代理地址格式

**HTTP 代理**:
```
http://192.168.1.100:7890
http://127.0.0.1:7890
http://proxy.yourcompany.com:8080
```

**SOCKS5 代理**:
```
socks5://192.168.1.100:1080
socks5://127.0.0.1:1080
```

### 如何找到你的代理？

**如果你使用 Clash/V2Ray 等工具**:
- 默认通常是：`http://127.0.0.1:7890`
- Clash 默认端口：7890
- V2Ray 默认端口：10808

**如果你在公司网络**:
- 询问网络管理员
- 查看浏览器代理设置
- 检查系统网络设置

**测试代理是否可用**:
```bash
# 测试代理
curl -I --connect-timeout 5 -x http://YOUR_PROXY:PORT https://www.baidu.com
```

---

## 2️⃣ 配置代理到脚本

编辑文件：`/app/working/stock_daily_site/generate_web_playwright.py`

找到这一行（约第 20 行）：
```python
PROXY = {
    'server': 'http://YOUR_PROXY_IP:YOUR_PROXY_PORT',
    # ...
}
```

修改为你的实际代理，例如：
```python
PROXY = {
    'server': 'http://192.168.1.100:7890',
    # 如果需要认证
    # 'username': 'myuser',
    # 'password': 'mypass123',
}
```

**保存文件**。

---

## 3️⃣ 安装 Playwright Chromium

### 方式 A：使用代理安装（推荐）

```bash
# 设置环境变量
export HTTP_PROXY="http://YOUR_PROXY:PORT"
export HTTPS_PROXY="http://YOUR_PROXY:PORT"

# 安装 Chromium
cd /app/working/stock_daily_site
playwright install chromium
```

### 方式 B：手动下载（如果安装失败）

1. 在其他能访问外网的机器下载：
   - 访问：https://playwright.azureedge.net/builds/chromium/1208/chromium-linux.zip
   - 下载约 200MB

2. 上传到服务器：
```bash
# 上传到 ~/.cache/ms-playwright/
mkdir -p ~/.cache/ms-playwright
# 解压
unzip chromium-linux.zip -d ~/.cache/ms-playwright/
```

### 验证安装

```bash
python3 -c "from playwright.sync_api import sync_playwright; print('✅ Playwright 可用')"
```

---

## 4️⃣ 测试运行

```bash
cd /app/working/stock_daily_site
python3 generate_web_playwright.py
```

**预期输出**:
```
==================================================
🚀 股票热点日报 (Playwright + 代理)
==================================================
📊 使用 Playwright 获取板块数据...
   启动浏览器 (代理：http://192.168.1.100:7890)...
   访问：https://quote.eastmoney.com/...
   等待数据加载...
   提取数据...
   ✅ 获取到 8 个板块
      1. 人工智能：+3.50% (领涨：科大讯飞)
      2. 半导体：+2.80% (领涨：中芯国际)
      ...

✅ 生成首页
✅ 生成日报
✅ 保存数据
✅ 生成归档页

==================================================
✅ 完成！
==================================================
```

**检查数据文件**:
```bash
cat /app/working/stock_daily_site/data/20260301.json | jq .source
# 应该输出："playwright_with_proxy"
```

---

## 5️⃣ 更新定时任务

删除旧任务：
```bash
copaw cron list  # 查看任务 ID
copaw cron delete 旧任务 ID
```

创建新任务：
```bash
copaw cron create --type text --name "股票日报 (Playwright)" --cron "15 0 * * 1-5" --channel console --target-user default --target-session 1772357503087 --text "cd /app/working/stock_daily_site && python3 generate_web_playwright.py && git add . && git commit -m 'Daily update' && git push && python3 send_feishu.py"
```

---

## 🔍 故障排查

### 问题 1: 代理连接失败

**错误**: `Proxy connection failed`

**解决**:
1. 检查代理地址是否正确
2. 测试代理是否可用：
   ```bash
   curl -x http://YOUR_PROXY:PORT https://www.baidu.com
   ```
3. 确认代理服务正在运行

### 问题 2: Playwright 安装失败

**错误**: `Download failure`

**解决**:
1. 确保代理配置正确
2. 使用方式 B（手动下载）
3. 或者使用已有的浏览器：
   ```python
   # 修改脚本，使用系统 Chrome
   browser = p.chromium.launch(
       executable_path='/usr/bin/google-chrome',
       proxy=PROXY
   )
   ```

### 问题 3: 页面加载超时

**错误**: `TimeoutError: Timeout 30000ms exceeded`

**解决**:
1. 增加超时时间：
   ```python
   page.goto(url, timeout=60000)
   ```
2. 检查网络连接
3. 尝试降低 `wait_until` 要求：
   ```python
   page.goto(url, wait_until='domcontentloaded')
   ```

### 问题 4: 数据解析失败

**错误**: 获取到空数据

**解决**:
1. 检查网页结构是否变化
2. 使用 headed 模式调试：
   ```python
   browser = p.chromium.launch(headless=False)  # 显示浏览器
   ```
3. 查看实际页面 HTML：
   ```python
   page.screenshot(path='debug.png')  # 截图
   print(page.content())  # 打印 HTML
   ```

---

## 📝 快速配置脚本

创建一个快速配置脚本 `setup.sh`:

```bash
#!/bin/bash
# 快速配置代理和 Playwright

# 1. 设置代理
export HTTP_PROXY="http://YOUR_PROXY:PORT"
export HTTPS_PROXY="http://YOUR_PROXY:PORT"

echo "✅ 代理配置：$HTTP_PROXY"

# 2. 安装 Playwright
echo "📦 安装 Playwright..."
pip install playwright -q
playwright install chromium

# 3. 测试
echo "🧪 测试运行..."
cd /app/working/stock_daily_site
python3 generate_web_playwright.py

echo "✅ 完成！"
```

---

## ✅ 完成检查清单

- [ ] 获取到代理地址
- [ ] 修改了 `generate_web_playwright.py` 中的 PROXY 配置
- [ ] 成功安装 Playwright Chromium
- [ ] 测试运行成功，获取到真实数据
- [ ] 数据文件 source 字段为 `playwright_with_proxy`
- [ ] 更新了定时任务
- [ ] 飞书推送正常

---

## 🎯 需要帮助？

如果遇到问题，请提供：
1. 错误信息（完整输出）
2. 你的代理地址格式
3. 网络环境（公司/家庭/其他）

我会帮你解决！🚀
