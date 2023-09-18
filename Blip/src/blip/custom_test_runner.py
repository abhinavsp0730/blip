from functools import partial
from unittest import TextTestResult, TextTestRunner

import httpretty
from django.test.runner import DiscoverRunner, RemoteTestResult

from .service import BlipService

blip_obj = BlipService()


class BlipTestRunnerRemoteTestResult(RemoteTestResult):
    def startTest(self, test):
        super().startTest(test)
        httpretty.reset()
        if blip_obj.blip_silently_bypass:
            blip_obj.register_httpretty_uri()
        httpretty.enable(allow_net_connect=False, verbose=blip_obj.blip_verbose)

    def stopTest(self, test):
        super().stopTest(test)
        httpretty.disable()
        httpretty.reset()


class BlipTextTestResult(TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super(BlipTextTestResult, self).__init__(stream, descriptions, verbosity)

    def startTest(self, test):
        super(BlipTextTestResult, self).startTest(test)
        httpretty.reset()
        if blip_obj.blip_silently_bypass:
            blip_obj.register_httpretty_uri()
        httpretty.enable(allow_net_connect=False, verbose=blip_obj.blip_verbose)

    def stopTest(self, test):
        super(BlipTextTestResult, self).stopTest(test)
        httpretty.disable()
        httpretty.reset()


class BlipTextTestRunner(TextTestRunner):
    resultclass = BlipTextTestResult


class BlipTestRunner(DiscoverRunner):
    def __init__(self, **kwargs):
        super(BlipTestRunner, self).__init__(**kwargs)
        self.parallel_test_suite.runner_class = partial(  # Add this
            self.parallel_test_suite.runner_class,
            resultclass=BlipTestRunnerRemoteTestResult,
        )

    test_runner = BlipTextTestRunner
