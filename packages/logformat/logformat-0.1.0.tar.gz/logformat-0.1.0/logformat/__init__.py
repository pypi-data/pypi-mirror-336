import asyncio
import base64
import datetime
import functools
import json
import logging
import time
from typing import Callable, Never, cast


class LogfmtFormatter(logging.Formatter):
    converter = time.gmtime

    def __init__(self, process_id=False, process_name=False, thread_id=False, thread_name=False):
        """Initializes a logfmt formatter."""
        self._process_id = process_id
        self._process_name = process_name
        self._thread_id = thread_id
        self._thread_name = thread_name

    def format(self, record):
        fields: dict = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "level": record.levelname.lower(),
        }

        if record.name != "root":
            # omitting logger=root for readability
            fields['logger'] = record.name

        fields['msg'] = record.getMessage()

        for k, v in record.__dict__.items():
            # using getattr because of https://github.com/python/typeshed/issues/12136
            if k in getattr(logging.LogRecord, "__static_attributes__"):
                continue
            if k in ('time', 'msg'):
                continue

            # This mirrors the logic of https://github.com/go-logfmt/logfmt/blob/main/encode.go.
            k = ''.join(c for c in k if c > ' ' and c not in '="')
            if k == '':
                continue

            fields[k] = v

        if self._process_id:
            fields['process_id'] = record.process
        if self._process_name:
            fields['process_name'] = record.processName
        if self._thread_id:
            fields['thread_id'] = record.thread
        if self._thread_name:
            fields['thread_name'] = record.threadName
        if record.taskName:
            fields['task'] = record.taskName
        if record.exc_info:
            fields['traceback'] = self.formatException(record.exc_info)
        if record.stack_info:
            fields['stack'] = self.formatStack(record.stack_info)

        return ' '.join(f'{k}={_fmt_value(v)}' for k, v in fields.items())


def get_logger(name: str | None = None):
    return _Logger(logging.getLogger(name))


def _fmt_value(obj):
    if obj is None:
        value = "null"
    elif isinstance(obj, bool):
        value = str(obj).lower()
    elif isinstance(obj, bytes):
        value = base64.b64encode(obj).decode()
    elif isinstance(obj, datetime.datetime):
        value = obj.isoformat().replace('+00:00', 'Z')
    else:
        value = str(obj)

    # This mirrors the logic of https://github.com/go-logfmt/logfmt/blob/main/encode.go.
    if any(c <= ' ' or c in '="' for c in value):
        return json.dumps(value, ensure_ascii=False)
    else:
        return value


_never: Never = cast(Never, None)


class _Logger:
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def debug(
        self,
        msg: str,
        traceback=False,
        stack=False,
        time=_never,
        level=_never,
        process_id=_never,
        process_name=_never,
        thread_id=_never,
        thread_name=_never,
        task=_never,
        # Logger.makeRecord raises if any of logging.LogRecord.__static_attributes__ are in extra.
        args=_never,
        created=_never,
        exc_info=_never,
        exc_text=_never,
        filename=_never,
        funcName=_never,
        levelname=_never,
        levelno=_never,
        module=_never,
        msecs=_never,
        name=_never,
        pathname=_never,
        process=_never,
        processName=_never,
        relativeCreated=_never,
        stack_info=_never,
        taskName=_never,
        thread=_never,
        threadName=_never,
        **kwargs,
    ):
        self._logger.debug(msg, exc_info=traceback, stack_info=stack, extra=kwargs)

    def info(
        self,
        msg: str,
        traceback=False,
        stack=False,
        time=_never,
        level=_never,
        process_id=_never,
        process_name=_never,
        thread_id=_never,
        thread_name=_never,
        task=_never,
        # Logger.makeRecord raises if any of logging.LogRecord.__static_attributes__ are in extra.
        args=_never,
        created=_never,
        exc_info=_never,
        exc_text=_never,
        filename=_never,
        funcName=_never,
        levelname=_never,
        levelno=_never,
        module=_never,
        msecs=_never,
        name=_never,
        pathname=_never,
        process=_never,
        processName=_never,
        relativeCreated=_never,
        stack_info=_never,
        taskName=_never,
        thread=_never,
        threadName=_never,
        **kwargs,
    ):
        self._logger.info(msg, exc_info=traceback, stack_info=stack, extra=kwargs)

    def warning(
        self,
        msg: str,
        traceback=False,
        stack=False,
        time=_never,
        level=_never,
        process_id=_never,
        process_name=_never,
        thread_id=_never,
        thread_name=_never,
        task=_never,
        # Logger.makeRecord raises if any of logging.LogRecord.__static_attributes__ are in extra.
        args=_never,
        created=_never,
        exc_info=_never,
        exc_text=_never,
        filename=_never,
        funcName=_never,
        levelname=_never,
        levelno=_never,
        module=_never,
        msecs=_never,
        name=_never,
        pathname=_never,
        process=_never,
        processName=_never,
        relativeCreated=_never,
        stack_info=_never,
        taskName=_never,
        thread=_never,
        threadName=_never,
        **kwargs,
    ):
        self._logger.warning(msg, exc_info=traceback, stack_info=stack, extra=kwargs)

    def error(
        self,
        msg: str,
        traceback=False,
        stack=False,
        time=_never,
        level=_never,
        process_id=_never,
        process_name=_never,
        thread_id=_never,
        thread_name=_never,
        task=_never,
        # Logger.makeRecord raises if any of logging.LogRecord.__static_attributes__ are in extra.
        args=_never,
        created=_never,
        exc_info=_never,
        exc_text=_never,
        filename=_never,
        funcName=_never,
        levelname=_never,
        levelno=_never,
        module=_never,
        msecs=_never,
        name=_never,
        pathname=_never,
        process=_never,
        processName=_never,
        relativeCreated=_never,
        stack_info=_never,
        taskName=_never,
        thread=_never,
        threadName=_never,
        **kwargs,
    ):
        self._logger.error(msg, exc_info=traceback, stack_info=stack, extra=kwargs)

    # intentionally omitting critical ... just use errors

    def log_uncaught(self, f: Callable):
        """
        Wraps the given function to log an uncaught exception as an error with a traceback and raise SystemExit(1).

        Meant to be used as a decorator on the main function.
        """

        @functools.wraps(f)
        def sync_wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as exc:
                exc_str = self._stringify_exception(exc)
                self.error(f"unexpected exception: {exc_str}", traceback=True)
                raise SystemExit(1)

        @functools.wraps(f)
        async def async_wrapper(*args, **kwargs):
            try:
                return await f(*args, **kwargs)
            except Exception as exc:
                exc_str = self._stringify_exception(exc)
                self.error(f"unexpected exception: {exc_str}", traceback=True)
                raise SystemExit(1)

        if asyncio.iscoroutinefunction(f):
            return async_wrapper
        else:
            return sync_wrapper

    def _stringify_exception(self, exc: Exception):
        try:
            return str(exc)
        except Exception:
            self.warning("while logging unexpected exception str(exc) raised", traceback=True)

        try:
            return repr(exc)
        except Exception:
            self.warning("while logging unexpected exception repr(exc) raised", traceback=True)

        return '??? (str and repr failed)'
