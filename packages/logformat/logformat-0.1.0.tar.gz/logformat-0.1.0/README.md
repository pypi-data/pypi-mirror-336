# logformat - logfmt logging for Python

* implements the same value escaping as the [logfmt library] used by Grafana Loki
* implements a `logging.Formatter` so it works with any library using the standard library logging
* implements a convenience wrapper around `logging.Logging` for specifying structured fields via `kwargs`

```python
import logging

import logformat

logfmt_handler = logging.StreamHandler()
logfmt_handler.setFormatter(logformat.LogfmtFormatter())
logging.basicConfig(handlers=[logfmt_handler], level=logging.INFO)

logger = logformat.get_logger()

logger.warning("this seems off", some_id=33)
```

Will output a line like:

```
time=2025-03-23T06:21:36Z level=warning msg="this seems off" some_id=33
```

`exc_info` and `stack_info` are supported via `backtrace=True` and `stack=True`
(which will add same-named fields).

In the main method of a script you should always catch any exception and log
them as errors, so that unexpected errors show up properly in your log file.
This library makes this easy by providing a `log_uncaught` decorator:

```python
logger = logformat.get_logger()

@logger.log_uncaught
def run():
    # your script
    ...
```

This library intentionally doesn't provide any pretty terminal output but the
produced logs can be viewed with the [logfmt CLI] (since that tool again uses
the [logfmt library] that this library is compatible with).

## Alternatives

* structlog's `get_logger` returns `Any`.
  While there's a typed alternative that's a bit of a footgun.

* logfmter doesn't include the time by default, names the time field `when` by default
  and the level field `at` by default, doesn't use ISO dates by default
  and isn't compatible with the Go [logfmt library] as of March 2025

[logfmt library]: https://github.com/go-logfmt/logfmt
[logfmt CLI]: https://github.com/TheEdgeOfRage/logfmt
