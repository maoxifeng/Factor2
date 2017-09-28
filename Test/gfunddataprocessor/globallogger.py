# coding: utf-8

import logging
import logging.config
import os

conf_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'logger.conf')

logging.config.fileConfig(conf_path)

logger = logging.getLogger()
