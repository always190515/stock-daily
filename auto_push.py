#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 自动推送脚本
使用方法：python3 auto_push.py YOUR_GITHUB_TOKEN
"""

import os
import sys
import subprocess
import json

REPO_OWNER = "always190515"
REPO_NAME = "stock-daily"
SITE_DIR = "/app/working/stock_daily_site"

def run_command(cmd, cwd=None):
    """运行 shell 命令"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd or SITE_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("=" * 60)
    print("🚀 GitHub 自动推送工具")
    print("=" * 60)
    
    # 获取 token
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        print("\n❌ 请提供 GitHub Personal Access Token")
        print("\n使用方法:")
        print(f"python3 {sys.argv[0]} ghp_xxxxxxxxxxxx")
        print("\n获取 Token 步骤:")
        print("1. 访问：https://github.com/settings/tokens/new")
        print("2. Token 名称：stock-daily-deploy")
        print("3. 权限：勾选 'repo'")
        print("4. 点击 'Generate token'")
        print("5. 复制 token（以 ghp_ 开头）")
        return False
    
    if not token.startswith("ghp_"):
        print("\n❌ Token 格式错误，应该以 'ghp_' 开头")
        return False
    
    print(f"\n✅ Token 已接收：{token[:8]}...{token[-4:]}")
    
    # 设置远程仓库 URL（带 token）
    print("\n📋 配置远程仓库...")
    remote_url = f"https://{REPO_OWNER}:{token}@github.com/{REPO_OWNER}/{REPO_NAME}.git"
    
    success, stdout, stderr = run_command(f"git remote set-url origin {remote_url}")
    if not success:
        print(f"❌ 配置失败：{stderr}")
        return False
    print("✅ 远程仓库配置完成")
    
    # 推送代码
    print("\n📤 正在推送代码到 GitHub...")
    success, stdout, stderr = run_command("git branch -M main")
    if not success and "already exists" not in stderr:
        print(f"⚠️ 分支设置警告：{stderr}")
    
    success, stdout, stderr = run_command("git push -u origin main")
    
    if success:
        print("\n" + "=" * 60)
        print("✅ 推送成功！")
        print("=" * 60)
        print(f"\n📱 仓库地址：https://github.com/{REPO_OWNER}/{REPO_NAME}")
        print("\n🎯 下一步：部署到 Vercel")
        print("1. 访问：https://vercel.com")
        print("2. 用 GitHub 登录")
        print("3. New Project -> 选择 'stock-daily'")
        print("4. 点击 'Deploy'")
        print("\n🎉 完成！")
        return True
    else:
        print(f"\n❌ 推送失败：{stderr}")
        print("\n可能的原因:")
        print("1. Token 无效或已过期")
        print("2. Token 没有 repo 权限")
        print("3. 网络连接问题")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
