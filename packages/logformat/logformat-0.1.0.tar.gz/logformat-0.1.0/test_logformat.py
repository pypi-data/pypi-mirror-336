#!/usr/bin/env python3
import asyncio
import contextlib
import datetime
import functools
import io
import logging
import textwrap
import unittest
import unittest.mock

import logformat


def set_up(level=logging.DEBUG):
    stream = io.StringIO()
    logfmt_handler = logging.StreamHandler(stream)
    logfmt_handler.setFormatter(logformat.LogfmtFormatter())
    logging.basicConfig(handlers=[logfmt_handler], level=level, force=True)
    return stream


# We're not using pytest here because pytest messes with the logging config,
# setting it's own handlers, apparently even when disabling the pytest logging
# plugin with `-p no:logging`.
test_suite = unittest.TestSuite()


def test(test):
    @functools.wraps(test)
    def wrapped_test():
        t = unittest.TestCase()
        with unittest.mock.patch("time.time_ns", return_value=1742634901036965331):
            test(t)

    test_suite.addTest(unittest.FunctionTestCase(wrapped_test))


@test
def test_logformat(t: unittest.TestCase):
    stream = set_up()
    logger = logformat.get_logger()
    logger.debug("what's happening")
    logger.info("something's happening")
    logger.warning("this seems off")
    logger.error("oh no")
    t.assertEqual(
        stream.getvalue(),
        textwrap.dedent(
            '''
            time=2025-03-22T09:15:01Z level=debug msg="what's happening"
            time=2025-03-22T09:15:01Z level=info msg="something's happening"
            time=2025-03-22T09:15:01Z level=warning msg="this seems off"
            time=2025-03-22T09:15:01Z level=error msg="oh no"
            '''
        ).lstrip(),
    )


@test
def test_escaping(t: unittest.TestCase):
    stream = set_up()
    logger = logformat.get_logger()
    logger.warning(" \t\n\x00='\"‽")
    t.assertEqual(
        stream.getvalue(),
        'time=2025-03-22T09:15:01Z level=warning msg=" \\t\\n\\u0000=\'\\"‽"\n',
    )


@test
def test_fmtlogger_extra_uses_str(t: unittest.TestCase):
    class Foo:
        def __str__(self):
            return "hello!"

    stream = set_up()
    logger = logformat.get_logger()
    logger.warning("test", value=Foo())
    t.assertEqual(
        stream.getvalue(),
        'time=2025-03-22T09:15:01Z level=warning msg=test value=hello!\n',
    )


@test
def test_fmtlogger_extra_none(t: unittest.TestCase):
    stream = set_up()
    logger = logformat.get_logger()
    logger.warning("test", helpful_info=None)
    t.assertEqual(
        stream.getvalue(),
        'time=2025-03-22T09:15:01Z level=warning msg=test helpful_info=null\n',
    )


@test
def test_fmtlogger_extra_bool(t: unittest.TestCase):
    stream = set_up()
    logger = logformat.get_logger()
    logger.warning("test", off_by_one=True)
    t.assertEqual(
        stream.getvalue(),
        'time=2025-03-22T09:15:01Z level=warning msg=test off_by_one=true\n',
    )


@test
def test_fmtlogger_extra_datetime(t: unittest.TestCase):
    stream = set_up()
    logger = logformat.get_logger()
    logger.warning(
        "test",
        expiry=datetime.datetime(2025, 3, 22, 15, 30, 00, 00, tzinfo=datetime.UTC),
    )
    t.assertEqual(
        stream.getvalue(),
        'time=2025-03-22T09:15:01Z level=warning msg=test expiry=2025-03-22T15:30:00Z\n',
    )


@test
def test_stdlib_logger(t: unittest.TestCase):
    stream = set_up()
    logger = logging.getLogger()
    logger.debug("what's happening %s", 1234)
    logger.info("something's happening")
    logger.warning("this seems off")
    logger.error("oh no")
    logger.critical("aaaaaaaaah!")
    t.assertEqual(
        stream.getvalue(),
        textwrap.dedent(
            '''
            time=2025-03-22T09:15:01Z level=debug msg="what's happening 1234"
            time=2025-03-22T09:15:01Z level=info msg="something's happening"
            time=2025-03-22T09:15:01Z level=warning msg="this seems off"
            time=2025-03-22T09:15:01Z level=error msg="oh no"
            time=2025-03-22T09:15:01Z level=critical msg=aaaaaaaaah!
            '''
        ).lstrip(),
    )


@test
def test_log_uncaught_sync_returns(t: unittest.TestCase):
    stream = set_up()

    logger = logformat.get_logger()

    @logger.log_uncaught
    def run():
        return 42

    t.assertEqual(run(), 42)
    t.assertEqual(stream.getvalue(), "")


@test
def test_log_uncaught_sync_raises(t: unittest.TestCase):
    stream = set_up()

    logger = logformat.get_logger()

    @logger.log_uncaught
    def run():
        5 / 0

    with t.assertRaises(SystemExit), stub_traceback():
        run()

    t.assertEqual(
        stream.getvalue(),
        'time=2025-03-22T09:15:01Z level=error msg="unexpected exception: division by zero" traceback="stub traceback"\n',
    )


@test
def test_log_uncaught_async_returns(t: unittest.TestCase):
    stream = set_up(level=logging.INFO)

    logger = logformat.get_logger()

    @logger.log_uncaught
    async def run():
        return 42

    t.assertEqual(asyncio.run(run()), 42)
    t.assertEqual(stream.getvalue(), "")


@test
def test_log_uncaught_async_raises(t: unittest.TestCase):
    stream = set_up(level=logging.INFO)

    logger = logformat.get_logger()

    @logger.log_uncaught
    async def run():
        5 / 0

    with t.assertRaises(SystemExit), stub_traceback():
        asyncio.run(run())

    t.assertEqual(
        stream.getvalue(),
        'time=2025-03-22T09:15:01Z level=error msg="unexpected exception: division by zero" task=Task-4 traceback="stub traceback"\n',
    )


@contextlib.contextmanager
def stub_traceback():
    def stub_print_exception(*args, **kwargs):
        kwargs['file'].write('stub traceback')

    with unittest.mock.patch("traceback.print_exception", stub_print_exception):
        yield


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(test_suite)
