# coding: utf-8


import os
import multiprocessing
import re
from subprocess import Popen
import sys
import time
import subprocess
import signal


sys.path.append(os.path.dirname(__file__))

from tests import initializetest, BaseLiveTestCase

__author__ = 'user'


class BaseProtractorTestCase(BaseLiveTestCase):

    def run_test(self, path_test):
        path = os.path.dirname(__file__)
        proc = Popen("protractor %s" % os.path.join(path, "all", path_test), shell=True, stdout=subprocess.PIPE)
        proc.wait()
        self._calc_output(proc.stdout.readlines())

    def _calc_output(self, outps):
        outs = outps
        output_string = ""

        results = filter(lambda x: "test" in x and "assert" in x and "failur" in x, outs)[0]
        tests, assertion, failures = map(int, re.search(r"(?:(\d+) test).*(?:(\d+) assert).*(?:(\d+) failur)", results).groups())
        if failures:

            f_start = filter(lambda x: "Failures:" in x, outs)[0]
            index_start = outs.index(f_start)
            output_string += f_start
            index = index_start
            try:
                cnt = 0
                while True:
                    index += 1
                    if outs[index] == "\n\t":
                        cnt += 1
                        if cnt > 1:
                            break
                    else:
                        output_string += outs[index]
                        pass
                    pass
            except IndexError:
                pass
        self.assertEqual(failures, 0, output_string)

    def __call__(self, result=None):
        try:

            res = self.process_webdr = Popen("webdriver-manager start", shell=True, stdout=subprocess.PIPE, stderr=None)
            time.sleep(1)
            out = res.stdout.readline()
            out = out.split("pid: ")
            self.pid_wd = int(out[1].replace("\n", ""))

            initializetest(self.application)
            self.port = 5674

            worker = lambda app, port: app.run(port=port)

            self._process = multiprocessing.Process(
                target=worker, args=(self.application, self.port)
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
