from plugins.others import *


class Problem:
    def __init__(self, data):
        """
        contestId： 比赛id
        index：题目序号（如：A、B、C。。。）
        name：题目名称
        rating：题目在cf上的rating
        tags：题目tag
        """

        self.contestId = data.get('contestId')
        self.index = data.get('index')
        self.name = data.get('name')
        self.rating = data.get('rating')
        self.tags = data.get('tags')


class Results:
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

        if self.creationTimeSeconds:
            self.time = get_time(self.creationTimeSeconds)
