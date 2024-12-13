from typing import TypeVar, Union

T = TypeVar('T')


class Result[T]:
    def __init__(self, value: Union[T, None] = None, error: Union[Exception, None] = None):
        self._value = value
        self._error = error

    @classmethod
    def Ok(cls, value: T):
        return cls(value=value)

    @classmethod
    def Err(cls, error: Exception):
        return cls(error=error)

    def is_ok(self) -> bool:
        return self._error is None

    def is_error(self) -> bool:
        return self._error is not None

    def value(self) -> T:
        return self._value

    def error(self) -> str:
        return str(self._error)

    def unwrap(self) -> Union[T, Exception]:
        return self._value if self.is_ok() else self._error

    def unwrap_or(self, default: T) -> T:
        return self._value if self.is_ok() else default
