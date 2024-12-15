import codeforces.api as cf_api
import codeforces.types as cf_types
import atcoder.api as at_api
import atcoder.types as at_types

from plugins.commands import Commands
from plugins.errors import *
from plugins.Result import Result

BOOLEANS = ["0", "1"]

AT_CONTEST_TYPES = ["abc", "arc"]
AT_INDEXS = ["A", "B", "C", "D", "E", "F", "G"]


async def user_cf_ac_problems(content: list[str]) -> Result[str]:
    # content：[command, <cf名称>, <查询提交个数>]
    command = Commands.CF_recent_ac

    try:
        user, num = content[1], int(content[2])
    except ValueError:
        return Result.Err(CommandError(command))

    if len(content) != 3:
        return Result.Err(CommandError(command))

    result = await cf_api.get_user_ac_problems(content[1], num)

    if result.is_error():
        return Result.Err(result.exception())
    else:
        res: str = ""
        problems: list[cf_types.Problem] = result.value()
        if len(problems) != 0:
            res += f"{user} 近期ac的题目有以下几个：\n"
            for p in problems:
                res += f"CF{p.contestId}{p.index} - {p.name} - rating:{p.rating}\n"
        else:
            res += f"nb，{user} 最近是没ac过吗\n"
        return Result.Ok(res)


async def at_random_problem_by_index(content: list[str]) -> Result[str]:
    # content：[command, <选择场次: (abc, arc)>, <序号: (A,B,C,D,E,F,G)>, <at名称>, <是否可以抽已经ac的题: (0,1)>]
    command = Commands.AT_random_problem_by_index
    contest_type, index, user, can_aced = content[1], content[2], content[3], content[4]

    if (
            len(content) != 5 or
            contest_type not in AT_CONTEST_TYPES or
            index not in AT_INDEXS or
            can_aced not in BOOLEANS
    ):
        return Result.Err(CommandError(command))

    can_aced = True if can_aced == "1" else False  # 是否可以抽已经 ac 的题
    result = await at_api.get_random_problem_by_index(contest_type, index, user, can_aced)

    if result.is_error():
        return Result.Err(result.exception())
    else:
        res = "以下是给您抽的题目：\n"
        problem: at_types.Problem = result.value()
        res += problem.get_secret_link()  # 返回题目链接
        return Result.Ok(res)


async def at_duel(content: list[str]) -> Result[str]:
    command = Commands.AT_duel
    pass
