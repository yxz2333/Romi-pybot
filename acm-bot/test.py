import asyncio
from atcoder.api import *
import atcoder_cpp_api


async def main():
    contest_type, index, user, can_aced = "abc", "A", "yxz2333", False
    all_problems, all_submissions = await asyncio.gather(fetch_problems(), fetch_all_submissions(user))
    results = atcoder_cpp_api.get_random_problem_by_index(all_problems, all_submissions, contest_type, index, can_aced)
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
