import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
import glob

url = "http://127.0.0.1:7001/bbs/login"

data = {
    "account": "admin",
    "password": "12345678"
}

headers = {
    "Content-Type": "application/json"
}


def send_request():
    start_time = time()
    response = requests.post(url, data=json.dumps(data), headers=headers)
    elapsed_time = time() - start_time
    response_json = response.json()
    return response_json, elapsed_time


# 自定义并发数和请求总数
concurrency = 10
n = 100

# 获取当前轮数
log_files = glob.glob("output*.log")
count = len(log_files) + 1

with ThreadPoolExecutor(concurrency) as executor:
    futures = [executor.submit(send_request) for _ in range(n)]

    success_count = 0
    error_count = 0
    total_elapsed_time = 0
    min_elapsed_time = float('inf')
    max_elapsed_time = float('-inf')

    for future in as_completed(futures):
        response_json, elapsed_time = future.result()
        total_elapsed_time += elapsed_time
        min_elapsed_time = min(min_elapsed_time, elapsed_time)
        max_elapsed_time = max(max_elapsed_time, elapsed_time)

        if response_json.get("code") == 200:
            success_count += 1
        elif response_json.get("code") == 0:
            error_count += 1

    avg_elapsed_time = total_elapsed_time / n

    output = f"""测试信息：
URL: {url}
数据: {json.dumps(data)}
并发数: {concurrency}
总请求数: {n}

结果：
成功响应: {success_count}
错误响应: {error_count}
平均响应时间: {avg_elapsed_time:.4f} 秒
最小响应时间: {min_elapsed_time:.4f} 秒
最大响应时间: {max_elapsed_time:.4f} 秒
"""

    print(output)

    # 将结果写入日志文件
    with open(f"output{count}.log", "w") as log_file:
        log_file.write(output)
