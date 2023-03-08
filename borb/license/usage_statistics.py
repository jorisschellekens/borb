#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class implements the basics for sending usage statistics to the borb server(s).
These kinds of checks are useful to get an idea of which functionality is most often used,
where development effort needs to be spent, etc
"""

import json
import sys
import threading
from datetime import datetime, timezone
import typing

import requests
from borb.license.anonymous_user_id import AnonymousUserID
from borb.license.version import Version


class UsageStatistics:
    """
    This class implements the basics for sending usage statistics to the borb server(s).
    These kinds of checks are useful to get an idea of which functionality is most often used,
    where development effort needs to be spent, etc
    """

    _ENDPOINT_URL: str = (
        "https://cztmincfqq4fobtt6c7ect7gli0isbwx.lambda-url.us-east-1.on.aws/"
    )

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def _send_usage_statistics_for_event(event: str, document: typing.Optional["Document"] = None) -> None:  # type: ignore[name-defined]

        # get anonymous_user_id
        anonymous_user_id: typing.Optional[str] = AnonymousUserID.get()
        if anonymous_user_id is None or len(anonymous_user_id) < 16:
            return

        # get number_of_pages
        number_of_pages: int = 0
        try:
            if document is not None:
                number_of_pages = int(
                    document.get_document_info().get_number_of_pages()
                )
        except:
            pass

        # set payload
        json_payload: typing.Dict[str, typing.Any] = {
            "anonymous_user_id": anonymous_user_id,
            "event": event,
            "number_of_pages": number_of_pages,
            "sys_platform": sys.platform,
            "utc_time_in_ms": int(datetime.now(timezone.utc).timestamp() * 1000),
            "version": Version.get_version(),
        }

        # set headers
        headers = {"Content-type": "application/json", "Accept": "text/plain"}

        # perform request
        try:
            requests.post(
                UsageStatistics._ENDPOINT_URL,
                headers=headers,
                data=json.dumps(json_payload),
            )
        except:
            pass

    #
    # PUBLIC
    #

    @staticmethod
    def disable() -> None:
        """
        This method disables the gathering of anonymous usage statistics
        :return:    None
        """
        AnonymousUserID.disable()

    @staticmethod
    def enable() -> None:
        """
        This method enables the gathering of anonymous usage statistics
        :return:    None
        """
        AnonymousUserID.enable()

    @staticmethod
    def send_usage_statistics(event: str, document: typing.Optional["Document"] = None) -> None:  # type: ignore[name-defined]
        """
        This method sends the usage statistics to the borb license server
        :param event:       the event that is to be registered
        :param document     the Document being processed
        :return:        None
        """
        try:
            threading.Thread(
                target=UsageStatistics._send_usage_statistics_for_event,
                args=(
                    event,
                    document,
                ),
            ).start()
        except:
            pass
