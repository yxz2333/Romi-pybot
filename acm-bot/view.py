from codeforces.api import get_user_ac_problems


async def handle_user_ac_problems(content: list[str]) -> str:
    # content：["/CF最近ac", <cf名称>, <查询提交个数>]
    cfid, num = content[1], int(content[2])

    result = await get_user_ac_problems(content[1], num)
    response = '\n'

    if result.is_error():
        response += result.error()
    else:
        problems = result.value()
        if problems:
            response += f"{cfid} 近期ac的题目有以下几个："
            for p in problems:
                response += f"\nCF{p.contestId}{p.index} - {p.name} - rating:{p.rating}"
        else:
            response += f"nb，{cfid} 最近是没ac过吗"
    return response
