class CustomError(Exception):
    def __init__(self, message="出错了"):
        self.message = message


class CommandError(CustomError):
    def __init__(self, command):
        super().__init__("指令用法错误")
        self.command = command

    def __str__(self):
        return f"{self.command}: {self.message}"


class QueryError(CustomError):
    """ 查询错误（Query）
    QueryError: "请求失败"
    QueryNotFound: "查询不到"
    QueryLargeNum: "查询数目过大"
    """

    def __init__(self, command: str, message: str = "请求失败"):
        super().__init__(message)
        self.command = command

    def __str__(self):
        return f"{self.command}: {self.message}"


class QueryNotFound(QueryError):
    def __init__(self, command: str, target: str = ''):
        super().__init__(command, "查询不到")
        self.target = target

    def __str__(self):
        return f"{self.command}: {self.message}{f" {self.target}" if self.target else ""}"


class QueryLargeNum(QueryError):
    def __init__(self, command: str, num: int):
        super().__init__(command, "查询数目过大")
        self.num = num

    def __str__(self):
        return f"{self.command}: {self.message}，不得超过 {self.num} 个"
