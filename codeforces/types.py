from plugins.others import *
from plugins.types import *


class Problem(ProblemType):
    def __init__(self, data):
        """
        name：题目名称
        contestId：比赛id
        index：题目序号（如：A、B、C。。。）
        rating：题目在cf上的rating
        tags：题目tag
        """

        super().__init__(data.get("name"))

        self.contestId = data.get('contestId')
        self.index = data.get('index')
        self.rating = data.get('rating')
        self.tags = data.get('tags')

    def get_link(self):
        return f'https://codeforces.com/contest/{self.contestId}/problem/{self.index}'


class Submission(SubmissionType):
    def __init__(self, data):
        """
        id：提交id
        creationTimeSeconds：提交时间（unix时间戳）
        problem：Problem对象
        programmingLanguage：编程语言
        verdict：提交状态
        passedTestCount：通过测试点个数
        timeConsumedMillis：运行时间（毫秒为单位）
        memoryConsumedBytes：运行内存（字节为单位）
        participantType：参加模式（练习、参赛者、VP）
        submitter：提交者，可以是一个队
        teamName：队名

        time：提交时间（北京时间）
        """

        self.id = data.get('id')
        self.creationTimeSeconds = data.get('creationTimeSeconds')
        self.problem = Problem(data.get('problem'))
        self.programmingLanguage = data.get('programmingLanguage')
        self.verdict = data.get('verdict')
        self.passedTestCount = data.get('passedTestCount')
        self.timeConsumedMillis = data.get('timeConsumedMillis')
        self.memoryConsumedBytes = data.get('memoryConsumedBytes')
        self.participantType = data.get('participantType')

        if "author" in data:
            if "members" in data['author']:
                self.submitter = [member.get('handle') for member in data['author']['members']]
            if "teamName" in data['author']:
                self.teamName = data['author']['teamName']

        if self.creationTimeSeconds is not None:
            super().__init__(get_time(self.creationTimeSeconds))
        else:
            super().__init__(None)

    def is_solved(self) -> bool:
        return self.verdict == 'OK'

    def get_result(self) -> str:
        return self.verdict

    def get_problem_id(self) -> str:
        return self.problem.name

    def get_problem_link(self) -> str:
        return self.problem.get_link()