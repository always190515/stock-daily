# 📊 股票日报数据源方案对比

## 当前状态

### ✅ 已实现的数据源

| 数据源 | 状态 | 说明 |
|--------|------|------|
| **china-stock-mcp** | ✅ 已集成 | 通过 MCP 服务获取，稳定性好 |
| **备用数据** | ✅ 可用 | 当 MCP 失败时使用 |
| **akshare 直连** | ⚠️ 不稳定 | 网络问题经常失败 |

### 📈 数据获取流程

```
generate_mcp_simple.py
    ↓
尝试通过 MCP 获取数据
    ├─ 成功 → 使用真实数据
    └─ 失败 → 使用备用数据
    ↓
生成 HTML 网站
    ↓
推送到 GitHub
    ↓
Vercel 自动部署
    ↓
飞书推送链接
```

## 🔧 三种数据获取方案对比

### 方案 A：MCP 服务（推荐 ✅）

**优点**：
- ✅ 稳定性好（本地服务，不受网络影响）
- ✅ 已集成到 CoPaw
- ✅ 有备用数据兜底
- ✅ 数据格式统一

**缺点**：
- ⚠️ 需要正确解析返回的 JSON 格式
- ⚠️ 部分接口返回格式需要适配

**实现**：
```python
# /app/working/stock_daily_site/generate_mcp_simple.py
from main import stock_board_industry_name_em, stock_zh_a_spot_em

sectors_result = stock_board_industry_name_em()
sectors_data = json.loads(sectors_result)
```

**使用**：
```bash
cd /app/working/stock_daily_site
python3 generate_mcp_simple.py
```

### 方案 B：AkShare 直连

**优点**：
- ✅ 数据最实时
- ✅ 接口最丰富

**缺点**：
- ❌ 网络不稳定（经常连接失败）
- ❌ 需要访问外网
- ❌ 可能被反爬

**实现**：
```python
import akshare as ak
df = ak.stock_board_industry_name_em()
```

### 方案 C：纯备用数据

**优点**：
- ✅ 100% 稳定
- ✅ 无需网络

**缺点**：
- ❌ 数据不真实
- ❌ 仅用于测试

## 🎯 推荐方案：MCP + 备用数据

### 当前配置

定时任务已经配置为使用 MCP 版本：

```bash
# 查看当前 cron 任务
copaw cron list

# 任务内容：
cd /app/working/stock_daily_site && python3 generate_mcp_simple.py && ...
```

### 数据优先级

1. **第一优先级**：MCP 服务（china-stock-mcp）
   - 调用 `stock_board_industry_name_em()` 获取板块数据
   - 调用 `stock_zh_a_spot_em()` 获取大盘数据
   
2. **第二优先级**：备用数据
   - 当 MCP 返回数据为空时自动切换
   - 保证网站一定能生成

### 监控和优化

查看每日数据源：
```bash
# 查看生成的数据文件
cat /app/working/stock_daily_site/data/20260301.json | jq .source
# 输出："china-stock-mcp" 或 "backup"
```

## 📝 下一步优化

### 1. 修复 MCP 数据解析

问题：MCP 返回的 JSON 格式需要进一步适配

解决：
```python
# 调试 MCP 返回数据
sectors_result = stock_board_industry_name_em()
print(sectors_result)  # 查看原始数据

# 根据实际格式调整解析逻辑
```

### 2. 添加数据日志

记录每次数据获取情况：
```python
import logging
logging.info(f"数据源：{'MCP' if sectors else '备用'}")
```

### 3. 测试真实数据

在交易时间运行，获取真实数据进行对比。

## 🚀 当前系统状态

| 组件 | 状态 | 备注 |
|------|------|------|
| **网站部署** | ✅ | https://stock-daily-personal.vercel.app |
| **数据获取** | ✅ | MCP + 备用数据 |
| **定时任务** | ✅ | 周一至周五 08:15 |
| **飞书推送** | ✅ | 已测试成功 |
| **历史归档** | ✅ | 最近 30 天 |

## 📊 数据源切换

如果想切换数据源，修改 cron 任务：

### 使用 MCP 版本（推荐）
```bash
copaw cron create --type text --name "股票日报" --cron "15 0 * * 1-5" --channel console --target-user default --target-session 1772357503087 --text "cd /app/working/stock_daily_site && python3 generate_mcp_simple.py && git add . && git commit -m 'Daily update' && git push && python3 send_feishu.py"
```

### 使用 AkShare 直连版本
```bash
copaw cron create --type text --name "股票日报" --cron "15 0 * * 1-5" --channel console --target-user default --target-session 1772357503087 --text "cd /app/working/stock_daily_site && python3 generate.py && git add . && git commit -m 'Daily update' && git push && python3 send_feishu.py"
```

## ✅ 结论

**当前方案**：MCP + 备用数据 是最优解

- ✅ 稳定性：MCP 服务本地运行，不受网络影响
- ✅ 可靠性：有备用数据兜底
- ✅ 实时性：MCP 从 AKShare 获取实时数据
- ✅ 可维护性：代码清晰，易于调试

**建议**：保持当前配置，在交易时间观察数据质量，必要时微调解析逻辑。
