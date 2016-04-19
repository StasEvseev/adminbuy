# coding: utf-8
__author__ = 'StasEvseev'

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


class BaseProtractorTestCase(BaseLiveTestCase):
    """
    Базовый класс тестов protractor.
    Запускает демона webdriver, тестовый проект и protractor.
    """

    port = 5674

    def __init__(self, *args, **kwargs):
        super(BaseProtractorTestCase, self).__init__(*args, **kwargs)
        self.pid_proj, self.pid_wd = None, None

    def run_test(self, path_test):
        #TODO сделать интерактив с webdriver
        path = os.path.dirname(__file__)
        proc = Popen("protractor %s" % os.path.join(path, "all", path_test), shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        res = []
        for it in iter(proc.stdout.readline, ''):
            res.append(it)
            sys.stdout.write(it)

        self._calc_output(res)

    def __call__(self, result=None):
        try:
            #Запускаем демона вебдрайвер
            #На вывод при запуске демон показывает pid
            res = self.process_webdr = Popen("webdriver-manager start", shell=True, stdout=subprocess.PIPE, stderr=None)
            time.sleep(1)
            out = res.stdout.readline()
            out = out.split("pid: ")
            #pid webdriver
            self.pid_wd = int(out[1].replace("\n", ""))

            #Создаем базу для тестов, прогоняем миграции
            initializetest(self.application)

            worker = lambda app, port: app.run(port=port)
            #Запускаем тестовую систему
            self._process = multiprocessing.Process(
                target=worker, args=(self.application, self.port)
            )
            self._process.start()
            self.pid_proj = self._process.pid

            time.sleep(1)

            super(BaseProtractorTestCase, self).__call__(result)
        finally:
            #По завершению тестов убираем за собой.
            if self.pid_wd:
                os.kill(self.pid_wd, signal.SIGKILL)
            if self.pid_proj:
                os.kill(self.pid_proj, signal.SIGKILL)

    def _calc_output(self, outps):
        """
        Анализируем вывод protractor.
        Если есть проваленные тесты - валим TestCase.
        """
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
            except IndexError:
                pass
        self.assertEqual(failures, 0)
