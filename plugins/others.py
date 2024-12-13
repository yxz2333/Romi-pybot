import time


## 获取当前时间
def get_time(timestamp=time.time()) -> str:
    # 传入时间戳
    local_time = time.localtime(timestamp)  # 将时间戳转换为本地时间结构
    formatted_time = time.strftime("%Y/%m/%d %H:%M", local_time)  # 格式化时间
    return formatted_time
