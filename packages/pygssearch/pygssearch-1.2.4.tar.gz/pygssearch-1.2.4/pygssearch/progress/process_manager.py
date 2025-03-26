# GAEL SYSTEMS CONFIDENTIAL
# __________________
#
# 2023 GAEL SYSTEMS
# All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of GAEL SYSTEMS,
# if any.  The intellectual and technical concepts contained
# herein are proprietary to GAEL SYSTEMS
# and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from GAEL SYSTEMS.
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger("pygssearch")


class ManagedPoolExecutor(ThreadPoolExecutor):
    """
    Managed Thread Pool Executor. A subclass of ThreadPoolExecutor.
    """
    def __init__(self, max_workers=2, fail_fast=False):
        ThreadPoolExecutor.__init__(self, max_workers=max_workers)
        self._futures = []
        self._excepts = []
        self._fail_fast = fail_fast

    def submit(self, fn, *args, **kwargs):
        future = super().submit(fn, *args, **kwargs)
        self._futures.append(future)
        return future

    def done(self):
        self._update()
        return len(self._futures) == 0

    def get_exceptions(self):
        return self._excepts

    def _update(self):
        for x in self._futures:
            if x.done():
                if x.exception():
                    if self._fail_fast:
                        self.shutdown(wait=True)
                    self._excepts.append(x.exception())
                    logger.error(x.exception())
                else:
                    name, start, end, writer = x.result()
                    logger.debug(f'Chunk Downloaded {name} [{start}, {end}]')
                self._futures.remove(x)
