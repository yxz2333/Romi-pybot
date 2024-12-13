import requests
from codeforces.types import Results, Problem
from plugins.Result import Result
from plugins.errors import *
from plugins.commands import Commands

URL = 'https://codeforces.com/api'
QUERY_NUM_LIMIT = 100  # 最大查询个数


async def get_user_status(user: str, num: int):
    # 获取 user 最近 num 个提交信息
    method = 'user.status'
    response = requests.get(f"{URL}/{method}?handle={user}&count={num}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


async def get_user_ac_problems(user: str, num: int) -> Result[list[Problem]]:
    # 获取 user 最近 num 个提交中 ac 的题目
    command = Commands.CF_recent_ac

    if num > QUERY_NUM_LIMIT:
        return Result.Err(QueryLargeNum(command, num))

    ans, err = [], None
    result = await get_user_status(user, num)
    if result:
        if result.get('status') == 'OK':
            for data in result.get('result'):
                res = Results(data)
                if res.verdict == 'OK':
                    ans.append(res.problem)
        else:
            err = QueryNotFound(command, user)
    else:
        err = QueryNotFound(command, user)

    return Result[list[Problem]](ans, err)
