import re

from django.conf import settings

from .constants import DEFAULT_BLIP_RESPONSE, DEFAULT_VERBOSE, DEFAULT_BLIP_STATUS_CODE, DEFAULT_SILENTLY_BYPASS


class BlipService:
    class BlipConfigIsNotDict(Exception):
        def __str__(self):
            return "BLIP_CONFIG must be a dict"

    def __init__(self):
        self.blip_config = {}
        try:
            self.blip_config = settings.BLIP_CONFIG
            if not isinstance(self.blip_config, dict):
                raise BlipService.BlipConfigIsNotDict
        except AttributeError:
            ...
        self.blip_status_code = self.blip_config.get("blip_status_code") or DEFAULT_BLIP_STATUS_CODE
        self.blip_response = self.blip_config.get("blip_response") or DEFAULT_BLIP_RESPONSE
        self.blip_verbose = self.blip_config.get("blip_verbose") or DEFAULT_VERBOSE
        self.blip_silently_bypass = self.blip_config.get("blip_silently_bypass") or DEFAULT_SILENTLY_BYPASS

    def register_httpretty_uri_and_update_cache_blip_obj(self, httpretty) -> None:
        http_pretty_methods = [httpretty.GET, httpretty.PUT, httpretty.POST, httpretty.DELETE, httpretty.HEAD,
                               httpretty.PATCH, httpretty.OPTIONS, httpretty.CONNECT]
        for http_pretty_method in http_pretty_methods:
            httpretty.register_uri(http_pretty_method, re.compile(r'.*'), body=self.blip_response,
                                   status=self.blip_status_code)
