from . import Verbosity, Logger, logged
from typing import Callable

"""
minlog test suite
run: poetry run python -m minlog._test
"""


def run_tests() -> None:
    """execute test suite with neat formatting"""

    logger = Logger()

    logger.be_debug()  # ensure full logging visibility

    # core logging functionality
    print("\n■ core logging")
    logger.debug("→ debug message")
    logger.trace("→ trace message")
    logger.info("→ info message")
    logger.warn("→ warning message")
    logger.error("→ error message")
    logger.crit("→ critical message")

    # verbosity controls
    print("\n■ verbosity handling")
    print("→ quiet mode (errors only)")
    logger.be_quiet()
    logger.info("• this should not appear")
    logger.error("• this error should appear")

    print("\n→ verbose mode (all messages)")
    logger.be_verbose()
    logger.debug("• debug should now appear")
    logger.info("• info should now appear")

    # source logging
    print("\n■ source loggers")
    app_logger = logger.logger_for("app")
    db_logger = logger.logger_for("db")
    app_logger.info("→ message from app context")
    db_logger.warn("→ warning from db context")

    # special cases
    print("\n■ special cases")
    print("→ rich formatting characters")
    logger.info("• message with [brackets]")
    logger.info("• message with [red]color[/red]")

    print("\n→ multi-line content")
    logger.info("• line one\n• line two")

    # message filtering
    print("\n■ message filtering")
    logger.be_quiet()
    logger.force_log("→ forced message in quiet mode")
    logger.log_only_when_quieter_than("→ conditional message", Verbosity.DEBUG)

    print("\n■ new verbosity helpers")
    print("→ check verbosity level")
    if logger.is_verbosity_above(Verbosity.ERROR):
        logger.error("• this should appear")
    else:
        logger.error("• this should not appear")

    print("→ temporary verbosity change")
    with logger.verbosity(Verbosity.DEBUG):
        logger.debug("• this debug message should appear")
        logger.trace("• this trace message should appear")

    # subsource context manager
    print("\n■ subsource context manager")
    with logger.subsource("soyjax"):
        logger.info("→ info message with subsource")
        logger.debug("→ debug message with subsource")

    # decorator usage
    print("\n■ logging decorator")

    @logged
    class MyClass:
        def do_something(self):
            self.logger.info("→ doing something in MyClass")

    @logged("custom_source")
    class MyOtherClass:
        def do_something(self):
            self.logger.info("→ doing something in MyOtherClass with custom source")

    my_instance = MyClass()
    my_instance.do_something()

    my_other_instance = MyOtherClass()
    my_other_instance.do_something()

    print("\n✓ all tests completed")


if __name__ == "__main__":
    run_tests()
