from src.orchestrator import DebugOrchestrator

# 模拟异常日志与相关代码
RAW_LOG = """
Traceback (most recent call last):
  File "sample_bug.py", line 9, in <module>
    print(divide_data([10, 20, 30], 0))
  File "sample_bug.py", line 3, in divide_data
    result = [d / divisor for d in data]
ZeroDivisionError: division by zero
"""

CODEBASE = '''
def divide_data(data, divisor):
    result = [d / divisor for d in data]
    return result
'''

if __name__ == "__main__":
    print("=" * 50)
    print("AutoDebug-MultiAgent 演示启动")
    print("=" * 50)
    
    orchestrator = DebugOrchestrator()
    result = orchestrator.run(RAW_LOG, CODEBASE)
    
    print("\n" + "=" * 50)
    print("最终输出：")
    print(f"根因分析：\n{result.get('root_cause', 'N/A')[:500]}...")
    print(f"生成补丁：\n{result.get('patch', 'N/A')[:500]}...")
    print(f"验证结果：{result.get('verify_result', 'N/A')}")
