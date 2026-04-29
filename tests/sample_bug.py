# 这是一个故意包含 Bug 的示例代码，用于演示
def divide_data(data, divisor):
    # Bug: 未处理 divisor 为 0 的情况
    result = [d / divisor for d in data]
    return result

# 触发异常
if __name__ == "__main__":
    print(divide_data([10, 20, 30], 0))
