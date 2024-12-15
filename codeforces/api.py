import json

import aiohttp
from typing import Union
from codeforces.types import *
from plugins.Result import Result
from plugins.errors import *
from plugins.commands import Commands

URL = 'https://codeforces.com/api'
QUERY_NUM_LIMIT = 100  # 最大查询个数


async def fetch_user_status(user: str, num: int) -> Union[str, None]:
    # 获取 user 最近 num 个提交信息
    method = 'user.status'

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{URL}/{method}?handle={user}&count={num}") as response:
            if response.status == 200:
                return await response.text()
            else:
                return None


async def get_user_ac_problems(user: str, num: int) -> Result[list[Problem]]:
    # 获取 user 最近 num 个提交中 ac 的题目
    command = Commands.CF_recent_ac

    if num > QUERY_NUM_LIMIT:
        return Result.Err(QueryLargeNum(command, num))

    result = await fetch_user_status(user, num)
    if result is None:
        return Result.Err(QueryError(command))

    ans, err = [], None
    result = json.loads(result)

    if result.get('status') == 'OK':
        for data in result.get('result'):
            res = Submission(data)
            if res.verdict == 'OK':
                ans.append(res.problem)
    else:
        err = QueryNotFound(command, user)

    return Result[list[Problem]](ans, err)
