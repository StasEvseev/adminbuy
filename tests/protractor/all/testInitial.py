# coding: utf-8
import os
import re
import subprocess
from tests.protractor.test import BaseProtractorTestCase
from subprocess import Popen

__author__ = 'user'


class TestProtractorInitial(BaseProtractorTestCase):
    def testA(self):
        path = os.path.dirname(__file__)

        proc = Popen("protractor %s" % os.path.join(path, "testInitial", "conf.js"), shell=True, stdout=subprocess.PIPE)
        proc.wait()
        outs = proc.stdout.readlines()
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