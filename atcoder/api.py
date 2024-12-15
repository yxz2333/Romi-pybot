import aiohttp
import asyncio
import json
from typing import Union
from atcoder.types import *
from plugins.Result import Result
from plugins.errors import *
from plugins.commands import Commands

import atcoder_cpp_api

INFORMATION_URL = 'https://kenkoooo.com/atcoder/resources'
STATISTICS_URL = 'https://kenkoooo.com/atcoder/atcoder-api/v3'


async def fetch_problems() -> Union[str, None]:
    # 获取 Atcoder 上全部的题
    obj = 'problems.json'

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{INFORMATION_URL}/{obj}") as response:
            if response.status == 200:
                return await response.text()
            else:
                return None


async def fetch_all_submissions(user: str) -> Union[str, None]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{STATISTICS_URL}/user/submissions?user={user}&from_second=0") as response:
            if response.status == 200:
                return await response.text()
            else:
                return None


async def get_random_problem_by_index(contest_type: str, index: str, user: str, can_aced: bool = False) -> \
        Result[Problem]:
    command = Commands.AT_random_problem_by_index

    problems_json = await fetch_problems()
    if problems_json is None:
        return Result.Err(QueryError(command))

    # 并发获取 atcoder 的全部题目 和 用户的全部提交
    all_problems, all_submissions = await asyncio.gather(fetch_problems(), fetch_all_submissions(user))
    res = json.loads(atcoder_cpp_api.get_random_problem_by_index(all_problems, all_submissions, contest_type, index, can_aced))

    err = res.get("error", None)
    if err is not None:
        if err == "cannot found":
            return Result.Err(QueryNotFound(command))
        else:
            return Result.Err(QueryError(command))

    return Result.Ok(Problem(res))


def get_duel_problem_by_index(contest_type: str, index: str, team_1: str, team_2: str, can_aced: bool = False) -> \
        Result[str]:
    command = Commands.AT_duel

    problems_json = fetch_problems()
    if problems_json is None:
        return Result.Err(QueryError(command))

    # 调用C++函数，传入json，C++函数返回题号
    # problem = random_single(contest_type, index, team_1, team_2, can_aced)
    pass
