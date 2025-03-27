import functools
import logging
from typing import Optional

from discord.ext.commands import Context
from discord.utils import MISSING
from zns_logging import ZnsLogger
from zns_logging.utility.LogHandlerFactory import LogHandlerFactory


class LoggerBase(ZnsLogger):
    """
    A class that extends ZnsLogger to provide flexible logging configurations.

    Args:
        reconnect (bool): Enables automatic reconnection when needed.
        log_handler (logging.Handler): The logging handler, default is determined if not provided.
        log_formatter (logging.Formatter): The log format, retrieved from the handler if not provided.
        log_level (int): The logging level.
        root_logger (bool): Specifies whether to use the root logger.
    """

    def __init__(
        self,
        reconnect: bool = True,
        log_handler: Optional[logging.Handler] = MISSING,
        log_formatter: logging.Formatter = MISSING,
        log_level: int = logging.INFO,
        root_logger: bool = False,
        **options,
    ):
        name, _, _ = __name__.partition('.')

        super().__init__(name, log_level, **options)

        self.reconnect = reconnect
        self.log_handler = log_handler
        self.log_formatter = log_formatter
        self.log_level = log_level
        self.root_logger = root_logger

        self._process_system_logger_params()

    def _process_system_logger_params(self):
        if not self.log_handler:
            self.log_handler = LogHandlerFactory.create_console_handler()

        if not self.log_formatter:
            self.log_formatter = self.log_handler.formatter

    @staticmethod
    def _create_send_log_method(log_level: str):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(self, ctx: Context, message: str):
                getattr(self, log_level)(f"Command log: {ctx.command.name} -> {message}")
                await ctx.send(content=message)
            return wrapper
        return decorator

    @staticmethod
    def _create_reply_log_method(log_level: str):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(self, ctx: Context, message: str):
                getattr(self, log_level)(f"Command log: {ctx.command.name} -> {message}")
                await ctx.reply(content=message)
            return wrapper
        return decorator

    @_create_send_log_method("debug")
    async def send_debug(self, ctx: Context, message: str): ...

    @_create_send_log_method("info")
    async def send_info(self, ctx: Context, message: str): ...

    @_create_send_log_method("warning")
    async def send_warning(self, ctx: Context, message: str): ...

    @_create_send_log_method("error")
    async def send_error(self, ctx: Context, message: str): ...

    @_create_send_log_method("critical")
    async def send_critical(self, ctx: Context, message: str): ...

    @_create_reply_log_method("debug")
    async def reply_debug(self, ctx: Context, message: str): ...

    @_create_reply_log_method("info")
    async def reply_info(self, ctx: Context, message: str): ...

    @_create_reply_log_method("warning")
    async def reply_warning(self, ctx: Context, message: str): ...

    @_create_reply_log_method("error")
    async def reply_error(self, ctx: Context, message: str): ...

    @_create_reply_log_method("critical")
    async def reply_critical(self, ctx: Context, message: str): ...
