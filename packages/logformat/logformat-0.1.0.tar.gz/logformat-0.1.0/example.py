#!/usr/bin/env python3
import json
import logging

import logformat
import requests


logfmt_handler = logging.StreamHandler()
logfmt_handler.setFormatter(logformat.LogfmtFormatter())
logging.basicConfig(handlers=[logfmt_handler], level=logging.DEBUG)


logger = logformat.get_logger()

requests.get('http://example.com')

logger.debug("what's happening")
logger.info("something's happening")
logger.warning("this seems off", some_id=33)
logger.error("oh no")

try:
    json.loads("maybe")
except:
    logger.error("failed to decode", traceback=True)
