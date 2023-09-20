import logging
import re
from dataclasses import dataclass
from typing import List

import httpretty
from django.conf import settings

from .constants import (
    DEFAULT_BLIP_RESPONSE,
    DEFAULT_VERBOSE,
    DEFAULT_BLIP_STATUS_CODE,
    DEFAULT_SILENTLY_BYPASS,
)

logger = logging.getLogger(__name__)


class BlipService:
    class BlipConfigIsNotDict(Exception):
        def __str__(self):
            return "BLIP_CONFIG must be a dict"

    @dataclass
    class BlipAdditionalGlobalMocks:
        request_uri: str
        request_method: str
        response_status_code: int
        response: str
        priority: int = 100

    def __init__(
        self,
        blip_status_code=DEFAULT_BLIP_STATUS_CODE,
        blip_response=DEFAULT_BLIP_RESPONSE,
        blip_verbose=DEFAULT_VERBOSE,
        blip_silently_bypass=DEFAULT_SILENTLY_BYPASS,
        blip_additional_global_mocks: List[BlipAdditionalGlobalMocks] = [],
    ):
        """
        Initialize BlipService with the given configuration.

        :param blip_status_code: Default status code for Blip responses.
        :param blip_response: Default Blip response.
        :param blip_verbose: Default verbosity level.
        :param blip_silently_bypass: Default silent bypass setting.
        :param blip_additional_global_mocks: List of additional global mock configurations.
        """
        self.blip_status_code = blip_status_code
        self.blip_response = blip_response
        self.blip_verbose = blip_verbose
        self.blip_silently_bypass = blip_silently_bypass
        self.blip_additional_global_mocks = blip_additional_global_mocks

    @classmethod
    def initialize_using_blip_config(cls):
        """
        Initialize BlipService using configuration from Django settings.

        :return: BlipService instance with settings.BLIP_CONFIG as the configuration.
        """
        blip_config = {}
        try:
            blip_config = settings.BLIP_CONFIG
            if not isinstance(blip_config, dict):
                raise BlipService.BlipConfigIsNotDict
        except AttributeError:
            pass
        return cls(**blip_config)

    @staticmethod
    def blip_httpretty_body_callback(response_body, status_code, http_method):
        """
        Callback function to handle HTTPretty registrations.

        :param response_body: Response body.
        :param status_code: HTTP status code.
        :param http_method: HTTP method (GET, PUT, POST, etc.).
        :return: Wrapper function for HTTPretty registration.
        """
        def wrapper(request, url, headers):
            logger.warning(
                f"Blip is using global mock for uri {url} with http method {http_method}"
            )
            return status_code, headers, response_body

        return wrapper

    def register_httpretty_uri(self) -> None:
        """
        Register URIs for HTTPretty mocking.

        Registers default global mock and additional global mocks.
        """
        http_pretty_methods = [
            httpretty.GET,
            httpretty.PUT,
            httpretty.POST,
            httpretty.DELETE,
            httpretty.HEAD,
            httpretty.PATCH,
            httpretty.OPTIONS,
            httpretty.CONNECT,
        ]

        # Register default HTTP methods
        for http_pretty_method in http_pretty_methods:
            httpretty.register_uri(
                http_pretty_method,
                re.compile(r".*"),
                body=BlipService.blip_httpretty_body_callback(
                    status_code=self.blip_status_code,
                    response_body=self.blip_response,
                    http_method=http_pretty_method,
                ),
            )

        # Register additional global mocks
        for additional_global_mock_dataclass in self.blip_additional_global_mocks:
            httpretty.register_uri(
                additional_global_mock_dataclass.request_method,
                additional_global_mock_dataclass.request_uri,
                body=BlipService.blip_httpretty_body_callback(
                    status_code=additional_global_mock_dataclass.response_status_code,
                    response_body=additional_global_mock_dataclass.response,
                    http_method=additional_global_mock_dataclass.request_method,
                ),
                priority=additional_global_mock_dataclass.priority,
            )
