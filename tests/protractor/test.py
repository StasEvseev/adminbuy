# coding: utf-8


import os
import multiprocessing
from subprocess import Popen
import sys
import time
import subprocess
import signal
from app import app


sys.path.append(os.path.dirname(__file__))

from tests import BaseTestCase

__author__ = 'user'


class BaseProtractorTestCase(BaseTestCase):

    def __call__(self, result=None):
        try:
            res = self.process_webdr = Popen("webdriver-manager start", shell=True, stdout=subprocess.PIPE, stderr=None)
            time.sleep(1)
            out = res.stdout.readline()
            out = out.split("pid: ")
            self.pid_wd = int(out[1].replace("\n", ""))

            worker = lambda app, port: app.run(port=port)

            self._process = multiprocessing.Process(
                target=worker, args=(app, 5674)
            )
            self._process.start()
            self.pid_proj = self._process.pid

            time.sleep(1)

            super(BaseProtractorTestCase, self).__call__(result)
        finally:
            if self.process_webdr:
                os.kill(self.pid_wd, signal.SIGKILL)
            if self._process:
                os.kill(self.pid_proj, signal.SIGKILL)