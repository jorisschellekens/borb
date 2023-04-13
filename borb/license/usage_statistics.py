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

from borb.license.license import License
from borb.license.machine_id import MachineID
from borb.license.persistent_random_user_id import PersistentRandomUserID
from borb.license.version import Version


class UsageStatistics:
    """
    This class implements the basics for sending usage statistics to the borb server(s).
    These kinds of checks are useful to get an idea of which functionality is most often used,
    where development effort needs to be spent, etc
    """

    # fmt: off
    _ENABLED: bool = True
    _ENDPOINT_URL: str = "https://cztmincfqq4fobtt6c7ect7gli0isbwx.lambda-url.us-east-1.on.aws/"
    # fmt: on

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def _get_machine_id() -> typing.Optional[str]:
        return MachineID.get()

    @staticmethod
    def _get_user_id() -> str:
        return License.get_user_id() or PersistentRandomUserID.get()

    @staticmethod
    def _send_usage_statistics_in_thread(event: str, document: typing.Optional["Document"] = None) -> None:  # type: ignore[name-defined]

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
            "anonymous_user_id": UsageStatistics._get_user_id(),
            "company": License.get_company(),
            "event": event,
            "license_valid_from_in_ms": License.get_valid_from_in_ms(),
            "license_valid_until_in_ms": License.get_valid_until_in_ms(),
            "machine_id": UsageStatistics._get_machine_id(),
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
        This function disables the sending of usage statistics
        :return:    None
        """
        UsageStatistics._ENABLED = False

    @staticmethod
    def enable() -> None:
        """
        This function enables the sending of usage statistics
        :return:    None
        """
        UsageStatistics._ENABLED = True

    @staticmethod
    def send_usage_statistics(event: str = "", document: typing.Optional["Document"] = None) -> None:  # type: ignore[name-defined]
        """
        This method sends the usage statistics to the borb license server
        :param event:       the event that is to be registered
        :param document     the Document being processed
        :return:        None
        """
        if not UsageStatistics._ENABLED:
            return
        try:
            threading.Thread(
                target=UsageStatistics._send_usage_statistics_in_thread,
                args=(
                    event,
                    document,
                ),
            ).start()
        except:
            pass
