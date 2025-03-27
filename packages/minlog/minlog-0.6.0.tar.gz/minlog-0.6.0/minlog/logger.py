import re
from contextlib import contextmanager
from functools import wraps
from typing import Optional, Type, TypeVar, Callable, Any, Generator, Union

from enum import Enum
from rich.console import Console
from typing import Optional


def to_snake_case(name: str) -> str:
    """convert camelcase/pascalcase to snake_case"""
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


T = TypeVar("T")


class Verbosity(Enum):
    """defines logging verbosity levels from most severe to most detailed"""

    CRITICAL = 0
    ERROR = 1
    WARN = 2
    INFO = 3
    TRACE = 4
    DEBUG = 5


class Logger:
    # mapping of verbosity levels to their short forms
    VERBOSITY_SHORTCUTS = {
        Verbosity.DEBUG: "dbg",
        Verbosity.TRACE: "trc",
        Verbosity.INFO: "inf",
        Verbosity.WARN: "wrn",
        Verbosity.ERROR: "err",
        Verbosity.CRITICAL: "crt",
    }

    # rich styling for different verbosity levels
    VERBOSITY_STYLES = {
        Verbosity.DEBUG: "bright_black on black",
        Verbosity.TRACE: "white on black",
        Verbosity.INFO: "green on black",
        Verbosity.WARN: "yellow on black",
        Verbosity.ERROR: "red on black",
        Verbosity.CRITICAL: "bright_red on black",
    }

    def __init__(
        self, verbosity: Verbosity = Verbosity.INFO, source: Optional[str] = None
    ):
        """initialize logger with given verbosity and optional source tag"""
        self._level = verbosity
        self._source = source
        self._subsource = None
        self._console = Console(stderr=True)

    def logger_for(self, source: str) -> "Logger":
        """create a new logger instance with the same verbosity but different source"""
        return Logger(self._level, source=source)

    def _format_message(self, message: str, level: Verbosity) -> tuple[str, str, str]:
        """format the message components with proper escaping"""
        # escape brackets to prevent rich interpretation
        meta = f"[{self.VERBOSITY_SHORTCUTS[level]}]".replace("[", "\\[")
        source = f"[{self._source}]" if self._source else ""
        if self._subsource:
            source = f"{source}:{self._subsource}"
        source = source.replace("[", "\\[") if source else ""
        content = message.replace("[", "\\[")
        return meta, source, content

    def log(self, message: str, level: Verbosity) -> None:
        """log a message with the specified verbosity level"""
        if level.value > self._level.value:
            return

        meta, source, content = self._format_message(message, level)

        # print components with appropriate styling
        self._console.print(meta, style=self.VERBOSITY_STYLES[level], end="")
        self._console.print(" ", end="")

        if source:
            self._console.print(source, style="bright_black", end=" ")

        self._console.print(content)

    # convenience methods for different log levels
    def debug(self, message: str) -> None:
        """log debug message"""
        self.log(message, Verbosity.DEBUG)

    def trace(self, message: str) -> None:
        """log trace message"""
        self.log(message, Verbosity.TRACE)

    def info(self, message: str) -> None:
        """log info message"""
        self.log(message, Verbosity.INFO)

    def warn(self, message: str) -> None:
        """log warning message"""
        self.log(message, Verbosity.WARN)

    def error(self, message: str) -> None:
        """log error message"""
        self.log(message, Verbosity.ERROR)

    def crit(self, message: str) -> None:
        """log critical message"""
        self.log(message, Verbosity.CRITICAL)

    # alias methods for convenience
    dbg = debug
    trc = trace
    inf = info
    wrn = warn
    err = error
    cri = crit

    def force_log(self, message: str) -> None:
        """force log a message at critical level"""
        self.crit(message)

    # verbosity control methods
    def is_quiet(self) -> bool:
        """check if logger is in quiet mode (error level)"""
        return self._level == Verbosity.ERROR

    def is_verbose(self) -> bool:
        """check if logger is in verbose mode (trace level)"""
        return self._level == Verbosity.TRACE

    def be_quiet(self) -> None:
        """set logger to quiet mode"""
        self._level = Verbosity.ERROR

    def be_verbose(self) -> None:
        """set logger to verbose mode"""
        self._level = Verbosity.TRACE

    def be_debug(self) -> None:
        """set logger to debug mode"""
        self._level = Verbosity.DEBUG

    def log_only_when_quieter_than(
        self, message: str, compare_verbosity: Verbosity
    ) -> None:
        """log message only if current verbosity is lower than specified level"""
        if self._level.value <= compare_verbosity.value:
            print(message)  # using standard print for this specific case

    @contextmanager
    def verbosity(self, level: Verbosity) -> Generator[None, None, None]:
        """temporarily change verbosity level"""
        original_level = self._level
        self._level = level
        try:
            yield
        finally:
            self._level = original_level

    @contextmanager
    def subsource(self, subsource: str) -> Generator[None, None, None]:
        """temporarily add a subsource to the log messages"""
        original_subsource = self._subsource
        self._subsource = subsource
        try:
            yield
        finally:
            self._subsource = original_subsource

    def is_verbosity_above(self, level: Verbosity) -> bool:
        """check if current verbosity is above given level"""
        return self._level.value >= level.value


def logged(
    source_or_class: Union[str, Type[T]],
) -> Union[Type[T], Callable[[Type[T]], Type[T]]]:
    """class decorator to add logging capability.
    can be used as @logged or @logged("custom_source")"""

    def decorator(cls: Type[T]) -> Type[T]:
        original_init = cls.__init__

        @wraps(original_init)
        def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
            # create logger before calling original __init__
            self.logger = logger.logger_for(
                source
                if isinstance(source_or_class, str)
                else to_snake_case(cls.__name__)
            )
            original_init(self, *args, **kwargs)

        cls.__init__ = new_init
        return cls

    # handle both @logged and @logged("source") cases
    if isinstance(source_or_class, str):
        source = source_or_class
        return decorator

    return decorator(source_or_class)


# create default logger instance
logger = Logger()
