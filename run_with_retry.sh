#!/bin/bash
# 股票日报网站任务 - 带重试机制的增强版执行脚本
# 文件名: run_with_retry.sh
# 用法：./run_with_retry.sh

set -e  # 有错误立即退出

# ════════════════════════════════════════════════
#                     配置选项
# ════════════════════════════════════════════════

# 基础配置
SITE_DIR="/app/working/stock_daily_site"
LOG_DIR="/app/working/logs"
MAX_RETRIES=3            # 最大重试次数
RETRY_DELAY=30          # 重试间隔(秒)
TASK_TIMEOUT=180        # 任务超时时间(秒)

# 邮件通知配置 (可选)
ENABLE_EMAIL_NOTIFY=false
EMAIL_RECIPIENT=""
EMAIL_SUBJECT="股票日报网站执行报告"

# ════════════════════════════════════════════════
#                     日志配置
# ════════════════════════════════════════════════

# 创建日志目录
mkdir -p "$LOG_DIR"

# 设置日志文件
TODAY=$(date +%Y%m%d)
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/stock_daily_${TODAY}.log"
EXEC_LOG="$LOG_DIR/stock_daily_exec_${TIMESTAMP}.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ ERROR: $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ SUCCESS: $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  WARNING: $1" | tee -a "$LOG_FILE"
}

# ════════════════════════════════════════════════
#                     工具函数
# ════════════════════════════════════════════════

# 检查依赖项
check_dependencies() {
    log "检查系统依赖项..."
    
    # 检查python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 未安装"
        return 1
    fi
    
    # 检查git
    if ! command -v git &> /dev/null; then
        log_error "Git 未安装"
        return 1
    fi
    
    # 检查目录
    if [ ! -d "$SITE_DIR" ]; then
        log_error "工作目录不存在: $SITE_DIR"
        return 1
    fi
    
    # 检查关键文件
    local required_files=("generate_mcp_simple.py" "send_feishu.py")
    for file in "${required_files[@]}"; do
        if [ ! -f "$SITE_DIR/$file" ]; then
            log_error "关键文件不存在: $SITE_DIR/$file"
            return 1
        fi
    done
    
    log_success "所有依赖项检查通过"
    return 0
}

# 检查网络连接
check_network() {
    log "检查网络连接..."
    
    # 测试百度连接
    if ! ping -c 2 baidu.com &> /dev/null; then
        log_warning "ping baidu.com 失败"
        return 1
    fi
    
    # 测试飞书API可达性
    if ! curl -s --max-time 10 https://open.feishu.cn > /dev/null; then
        log_warning "飞书API连接测试失败"
        return 1
    fi
    
    log_success "网络连接正常"
    return 0
}

# 执行单个步骤（带重试）
execute_with_retry() {
    local step_name="$1"
    local command="$2"
    local retries=0
    
    log "开始执行步骤: $step_name"
    
    while [ $retries -lt $MAX_RETRIES ]; do
        if [ $retries -gt 0 ]; then
            log_warning "第 $retries 次重试: $step_name"
            sleep $RETRY_DELAY
        fi
        
        log "执行命令: $command"
        
        # 设置超时执行
        if timeout $TASK_TIMEOUT bash -c "$command" 2>&1 | tee -a "$EXEC_LOG"; then
            log_success "步骤完成: $step_name"
            return 0
        else
            retries=$((retries + 1))
            if [ $retries -lt $MAX_RETRIES ]; then
                log_warning "步骤失败，将进行重试: $step_name"
            fi
        fi
    done
    
    log_error "步骤失败 (已重试 $MAX_RETRIES 次): $step_name"
    return 1
}

# 检查步骤结果
check_step_result() {
    local step_name="$1"
    local check_command="$2"
    
    log "检查步骤结果: $step_name"
    
    if eval "$check_command"; then
        log_success "步骤验证通过: $step_name"
        return 0
    else
        log_error "步骤验证失败: $step_name"
        return 1
    fi
}

# ════════════════════════════════════════════════
#                    主执行流程
# ════════════════════════════════════════════════

main() {
    local start_time=$(date +%s)
    
    log "╔══════════════════════════════════════════════╗"
    log "║   股票日报网站任务 - 增强版(带重试机制)      ║"
    log "║       开始时间: $(date '+%Y-%m-%d %H:%M:%S')         ║"
    log "╚══════════════════════════════════════════════╝"
    
    # 切换到工作目录
    cd "$SITE_DIR" || {
        log_error "无法切换到工作目录: $SITE_DIR"
        exit 1
    }
    
    # 1. 前置检查
    if ! check_dependencies; then
        log_error "依赖项检查失败，任务终止"
        exit 1
    fi
    
    if ! check_network; then
        log_warning "网络检查有警告，但继续执行"
    fi
    
    # 记录开始状态
    local initial_git_status=$(git status --short 2>/dev/null | wc -l)
    
    # 2. 主执行步骤（每个步骤都有重试机制）
    
    # 步骤1: 生成数据报告
    execute_with_retry "生成数据报告" "python3 generate_mcp_simple.py" || {
        log_error "数据报告生成失败，但继续尝试其他步骤"
    }
    
    # 验证文件生成
    TODAY=$(date +%Y%m%d)
    check_step_result "验证数据文件" "[ -f \"data/${TODAY}.json\" ]"
    check_step_result "验证HTML报告" "[ -f \"daily/${TODAY}.html\" ]"
    
    # 步骤2: Git操作
    execute_with_retry "Git添加文件" "git add ." || {
        log_error "Git添加失败，继续尝试提交"
    }
    
    # 检查是否有文件需要提交
    local changes=$(git status --short 2>/dev/null)
    if [ -n "$changes" ]; then
        local commit_msg="Daily update: $(date +%Y%m%d%H%M%S) - 股票日报网站"
        execute_with_retry "Git提交" "git commit -m \"$commit_msg\"" || {
            log_error "Git提交失败，检查是否需要强制推送"
        }
    else
        log "没有检测到文件变化，跳过Git提交"
    fi
    
    # 步骤3: Git推送（如果有提交）
    if [ -n "$changes" ] || git log --oneline -1 2>/dev/null | grep -q "Daily update"; then
        execute_with_retry "Git推送" "git push" || {
            log_warning "Git推送失败，可能是网络问题"
        }
    fi
    
    # 步骤4: 发送飞书通知
    execute_with_retry "发送飞书通知" "python3 send_feishu.py" || {
        log_error "飞书通知发送失败，但任务整体完成"
    }
    
    # 3. 后置检查和清理
    
    # 检查最终状态
    local final_git_status=$(git status --short 2>/dev/null | wc -l)
    
    # 统计执行时间
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    # 4. 生成摘要报告
    log ""
    log "╔══════════════════════════════════════════════╗"
    log "║               任务执行摘要                   ║"
    log "╠══════════════════════════════════════════════╣"
    log "║ 总执行时间: ${duration} 秒"
    log "║ 任务状态: $([ -f "daily/${TODAY}.html" ] && echo "✅ 成功" || echo "❌ 失败")"
    log "║ 生成的报告: $(find data/ daily/ -name \"${TODAY}.*\" 2>/dev/null | wc -l) 个文件"
    log "║ Git初始状态: ${initial_git_status} 个未跟踪文件"
    log "║ Git最终状态: ${final_git_status} 个未跟踪文件"
    log "╚══════════════════════════════════════════════╝"
    
    # 保存详细日志
    log "详细执行日志已保存到: $EXEC_LOG"
    log "每日日志汇总: $LOG_FILE"
    
    # 任务完成
    local return_code=0
    if [ ! -f "daily/${TODAY}.html" ]; then
        log_error "最终报告文件未生成，任务可能未完全成功"
        return_code=1
    else
        log_success "任务执行完成"
    fi
    
    return $return_code
}

# 执行主函数
main "$@"