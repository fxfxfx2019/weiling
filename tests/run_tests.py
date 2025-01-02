"""
运行所有测试
"""
import sys
import argparse

# 导入测试模块
from user_test.test_jwt_flow import test_jwt_flow
from user_test.test_user_api import test_user_api
from user_test.test_api_basic import test_user_flow
from user_test.test_user_concurrent import test_concurrent_users

def run_jwt_tests():
    """运行JWT认证测试"""
    print("\n=== JWT认证流程测试 ===\n")
    test_jwt_flow()

def run_user_api_tests():
    """运行用户API测试"""
    print("\n=== 用户API测试 ===\n")
    test_user_api()

def run_basic_api_tests():
    """运行基础API测试"""
    print("\n=== 基础API测试 ===\n")
    test_user_flow()

def run_concurrent_tests(user_count=100):
    """运行并发测试"""
    print(f"\n=== 并发测试（{user_count}用户）===\n")
    test_concurrent_users(user_count)

def main():
    parser = argparse.ArgumentParser(description="运行用户功能测试")
    parser.add_argument("--all", action="store_true", help="运行所有测试")
    parser.add_argument("--jwt", action="store_true", help="运行JWT认证测试")
    parser.add_argument("--user", action="store_true", help="运行用户API测试")
    parser.add_argument("--basic", action="store_true", help="运行基础API测试")
    parser.add_argument("--concurrent", type=int, help="运行并发测试，可指定用户数")
    
    args = parser.parse_args()
    
    # 如果没有指定任何参数，显示帮助信息
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    try:
        if args.all or args.jwt:
            run_jwt_tests()
        
        if args.all or args.user:
            run_user_api_tests()
        
        if args.all or args.basic:
            run_basic_api_tests()
        
        if args.all or args.concurrent is not None:
            user_count = args.concurrent if args.concurrent else 100
            run_concurrent_tests(user_count)
            
    except Exception as e:
        print(f"\n测试过程中出现错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 