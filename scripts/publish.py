#!/usr/bin/env python3
"""
项目发布脚本
用于自动化发布流程：测试 -> 构建 -> 发布
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"运行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result


def check_environment():
    """检查环境配置"""
    print("=== 环境检查 ===")
    
    # 检查Python版本
    version = sys.version_info
    if version < (3, 8):
        print("❌ 需要Python 3.8+")
        sys.exit(1)
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    
    # 检查必要工具
    tools = ['git', 'python', 'pip']
    for tool in tools:
        try:
            run_command(f"{tool} --version")
        except SystemExit:
            print(f"❌ 缺少工具: {tool}")
            sys.exit(1)


def run_tests():
    """运行测试"""
    print("=== 运行测试 ===")
    run_command("pytest tests/ -v --cov=visualization_toolkit")
    print("✅ 测试通过")


def build_package():
    """构建包"""
    print("=== 构建包 ===")
    
    # 清理旧构建
    run_command("rm -rf dist/ build/ *.egg-info/")
    
    # 构建
    run_command("python -m build")
    
    # 检查构建结果
    dist_files = list(Path("dist").glob("*.whl"))
    if not dist_files:
        print("❌ 构建失败")
        sys.exit(1)
    
    print("✅ 构建成功")
    for file in dist_files:
        print(f"  - {file}")


def publish_testpypi():
    """发布到TestPyPI"""
    print("=== 发布到TestPyPI ===")
    run_command("twine upload --repository testpypi dist/*")
    print("✅ 已发布到TestPyPI")


def publish_pypi():
    """发布到PyPI"""
    print("=== 发布到PyPI ===")
    run_command("twine upload dist/*")
    print("✅ 已发布到PyPI")


def create_git_tag(version):
    """创建Git标签"""
    print("=== 创建Git标签 ===")
    run_command(f"git tag -a v{version} -m 'Release version {version}'")
    run_command("git push origin --tags")
    print(f"✅ 已创建标签 v{version}")


def main():
    parser = argparse.ArgumentParser(description='发布项目')
    parser.add_argument('--test', action='store_true', help='仅测试')
    parser.add_argument('--testpypi', action='store_true', help='发布到TestPyPI')
    parser.add_argument('--pypi', action='store_true', help='发布到PyPI')
    parser.add_argument('--version', required=True, help='版本号')
    
    args = parser.parse_args()
    
    check_environment()
    run_tests()
    build_package()
    
    if args.test:
        print("✅ 测试完成")
        return
    
    if args.testpypi:
        publish_testpypi()
    
    if args.pypi:
        publish_pypi()
        create_git_tag(args.version)


if __name__ == "__main__":
    main()