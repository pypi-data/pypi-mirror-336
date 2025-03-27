# minlog

a neat and simple minimalistic logging library for python.

## installation

```bash
pip install minlog
```

## usage

```python
from minlog import Logger

# create a logger instance
my_logger = Logger()

# or use the global logger instance
from minlog import logger
my_logger = logger.logger_for("stuff")

# log messages with different severity levels
logger.debug("debugging info")
logger.trace("trace message")
logger.info("general information")
logger.warn("warning message")
logger.error("error condition")
logger.crit("critical failure")
```

## controlling verbosity

```python
# show only errors and critical messages
logger.be_quiet()

# show all messages including debug and trace
logger.be_verbose()

# show messages at debug level
logger.be_debug()

# temporarily change verbosity using context manager
with logger.verbosity(Verbosity.DEBUG):
    logger.debug("this will be shown")
    logger.trace("this too")

# conditional logging based on verbosity
if logger.is_verbosity_above(Verbosity.ERROR):
    logger.error("this will only show in verbose modes")
```

## source logging

organize logs by source/context:

```python
# create loggers for different components
app_logger = logger.logger_for("app")
db_logger = logger.logger_for("db")

app_logger.info("message from application")
db_logger.warn("database warning")

# temporary subsource context
with logger.subsource("api"):
    logger.info("message with api context")
```

## class decoration

automatically add logging to classes:

```python
from minlog import logged

@logged  # uses class name as source
class MyClass:
    def do_something(self):
        self.logger.info("doing something")

@logged("custom_source")  # specify custom source
class MyOtherClass:
    def do_something(self):
        self.logger.info("doing something else")
```

## advanced features

```python
# force a message regardless of verbosity
logger.force_log("important message")

# conditional logging based on verbosity threshold
logger.log_only_when_quieter_than("debug info", Verbosity.DEBUG)

# multi-line messages are supported
logger.info("line one\nline two")

# rich text formatting characters are handled correctly
logger.info("message with [brackets]")
logger.info("message with [red]color[/red]")
```
