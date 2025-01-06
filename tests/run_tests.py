"""
运行测试脚本
"""
import sys
import time
import argparse
from datetime import datetime

# 导入测试模块
from user_test.test_jwt_flow import test_jwt_flow
from user_test.test_user_api import test_user_api
from user_test.test_user_concurrent import test_concurrent_users

class TestReport:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.results = []
    
    def start(self):
        """开始测试"""
        self.start_time = time.time()
        print(f"\n=== 测试开始 === {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    def add_result(self, test_name, success, error=None):
        """添加测试结果"""
        self.results.append({
            "name": test_name,
            "success": success,
            "error": str(error) if error else None
        })
    
    def end(self):
        """结束测试并打印报告"""
        self.end_time = time.time()
        duration = round(self.end_time - self.start_time, 2)
        
        success_count = sum(1 for r in self.results if r["success"])
        total_count = len(self.results)
        
        print("\n=== 测试报告 ===\n")
        print(f"执行时间: {duration} 秒")
        print(f"总用例数: {total_count}")
        print(f"成功用例: {success_count}")
        print(f"失败用例: {total_count - success_count}")
        print(f"成功率: {(success_count/total_count*100):.1f}%\n")
        
        if total_count - success_count > 0:
            print("失败用例详情:")
            for result in self.results:
                if not result["success"]:
                    print(f"- {result['name']}: {result['error']}")
            print()

def run_jwt_tests(report):
    """运行JWT认证测试"""
    print("\n=== JWT认证流程测试 ===\n")
    try:
        test_jwt_flow()
        report.add_result("JWT认证测试", True)
    except Exception as e:
        report.add_result("JWT认证测试", False, e)

def run_user_api_tests(report):
    """运行用户API测试"""
    print("\n=== 用户API测试 ===\n")
    try:
        test_user_api()
        report.add_result("用户API测试", True)
    except Exception as e:
        report.add_result("用户API测试", False, e)

def run_concurrent_tests(report, user_count=10):
    """运行并发测试"""
    print(f"\n=== 并发测试（{user_count}用户）===\n")
    try:
        test_concurrent_users(user_count)
        report.add_result(f"并发测试({user_count}用户)", True)
    except Exception as e:
        report.add_result(f"并发测试({user_count}用户)", False, e)

def main():
    parser = argparse.ArgumentParser(description="运行用户认证测试")
    parser.add_argument("--all", action="store_true", help="运行所有测试")
    parser.add_argument("--jwt", action="store_true", help="运行JWT认证测试")
    parser.add_argument("--api", action="store_true", help="运行用户API测试")
    parser.add_argument("--concurrent", type=int, help="运行并发测试，可指定用户数")
    
    args = parser.parse_args()
    
    # 如果没有指定任何参数，显示帮助信息
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    report = TestReport()
    report.start()
    
    try:
        if args.all or args.jwt:
            run_jwt_tests(report)
        
        if args.all or args.api:
            run_user_api_tests(report)
        
        if args.all or args.concurrent is not None:
            user_count = args.concurrent if args.concurrent else 10
            run_concurrent_tests(report, user_count)
            
    except Exception as e:
        print(f"\n测试过程中出现错误: {str(e)}")
    finally:
        report.end()
        
        # 如果有测试失败，返回非零状态码
        if any(not r["success"] for r in report.results):
            sys.exit(1)

if __name__ == "__main__":
    main() 