from abc import ABC, abstractmethod


class ProblemType(ABC):
    def __init__(self, name):
        self.name = name

    def get_name(self) -> str:
        return self.name

    @abstractmethod
    def get_link(self) -> str:
        # 获取题目链接
        pass


class SubmissionType(ABC):
    def __init__(self, time):
        self.time = time

    def get_time(self) -> str:
        return self.time

    @abstractmethod
    def get_result(self) -> str:
        # 获取提交状态
        pass

    @abstractmethod
    def is_solved(self) -> bool:
        # 提交是否ac
        pass

    @abstractmethod
    def get_problem_id(self) -> str:
        # 获取提交的题目的id
        pass

    @abstractmethod
    def get_problem_link(self) -> str:
        # 获取提交的题目的链接
        pass
