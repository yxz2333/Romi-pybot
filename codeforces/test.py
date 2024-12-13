import asyncio

from api import *
from codeforces.types import Results


async def main():
    users = ['yxz2333', 'grieff']
    tasks = [asyncio.create_task(get_user_status(user, 10)) for user in users]
    results = await asyncio.gather(*tasks)
    for result in results:
        if result.get('status') == 'OK':
            for data in result.get('result'):
                res = Results(data)
                if res.verdict == 'OK':
                    print(res.problem.name)


if __name__ == '__main__':
    asyncio.run(main())