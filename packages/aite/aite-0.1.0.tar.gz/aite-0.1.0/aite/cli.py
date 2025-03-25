import argparse
import sys
from typing import List


def main(args: List[str] = None) -> int:
    """命令行入口函数"""
    parser = argparse.ArgumentParser(description="AITE - 人工智能测试与评估工具")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 添加子命令
    test_parser = subparsers.add_parser("test", help="运行测试")
    test_parser.add_argument("--type", choices=["fuzz", "attack", "vision"], required=True, help="测试类型")
    
    args = parser.parse_args(args)
    
    if args.command == "test":
        if args.type == "fuzz":
            print("执行模糊测试...")
        elif args.type == "attack":
            print("执行攻击测试...")
        elif args.type == "vision":
            print("执行视觉测试...")
    else:
        parser.print_help()
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 