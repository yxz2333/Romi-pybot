from plugins.others import *
from plugins.types import *


class Problem(ProblemType):
    def __init__(self, data):
        """
        name：题目名称
        id：总id
        contest_id：比赛id
        problem_index：题目序号（如：A、B、C。。。）
        """

        super().__init__(data.get("name"))

        self.id = data.get('id')
        self.contest_id = data.get('contest_id')
        self.problem_index = data.get('problem_index')

    def get_link(self) -> str:
        return f'https://atcoder.jp/contests/{self.contest_id}/tasks/{self.id}'

    def get_secret_link(self) -> str:
        return f'http请s://at删coder掉.j我p/contests/{self.contest_id}/tasks/{self.id}'


class Submission(SubmissionType):
    def __init__(self, data):
        """
        id：提交id
        epoch_second：提交时间（unix时间戳）
        problem_id：问题id
        contest_id：比赛id
        user_id：提交者id
        language：编程语言
        result：提交结果
        execution_time：运行时间

        time：提交时间（北京时间）
        link：题目链接
        """

        self.id = data.get('id')
        self.epoch_seconds = data.get('epoch_seconds')
        self.problem_id = data.get('problem_id')
        self.contest_id = data.get('contest_id')
        self.user_id = data.get('user_id')
        self.language = data.get('language')
        self.result = data.get('result')
        self.execution_time = data.get('execution_time')

        if self.execution_time is not None:
            super().__init__(get_time(self.execution_time))
        else:
            super().__init__(None)

    def is_solved(self) -> bool:
        return self.result == 'AC'

    def get_result(self) -> str:
        return self.result

    def get_problem_id(self) -> str:
        return self.problem_id

    def get_problem_link(self) -> str:
        return f'https://atcoder.jp/contests/{self.contest_id}/tasks/{self.id}'
