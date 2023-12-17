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
import time
import typing
from datetime import datetime
from datetime import timezone

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
    _FAIR_USE_LAST_INVOCATION_NUMBER_OF_DOCUMENTS: int = 0
    _FAIR_USE_LAST_INVOCATION_TIMESTAMP_IN_MS: int = 0
    _FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE: int = 100
    # fmt: on

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def _display_fair_use_warning() -> None:

        # never display this warning to a licensed user
        if License.get_user_id() is not None:
            return

        # fmt: off
        UsageStatistics._FAIR_USE_LAST_INVOCATION_NUMBER_OF_DOCUMENTS = 0
        print("\u001b[48;2;241;205;48mDear user,\n\n"
              "We noticed that you have exceeded the threshold of 100 documents per minute\n"
              "while using our Python PDF library. We're thrilled that our library is\n"
              "proving to be useful in your application!\n\n"
              "However, we want to bring to your attention the licensing terms of our\n"
              "library. It is dual licensed under AGPLv3 (GNU Affero General Public License,\n"
              "version 3) and a commercial license.\n\n"
              "If you are using our library for personal or non-commercial projects, you can\n"
              "continue to do so under the terms of the AGPLv3 license. We appreciate your\n"
              "support of open-source software.\n\n"
              "However, if you are using our library in a commercial setting, offering\n"
              "services or products to third parties, or if your usage does not abide by the\n"
              "AGPLv3 conditions, you are required to obtain a commercial license from us.\n"
              "This commercial license ensures compliance with the legal requirements and\n"
              "supports the ongoing development and maintenance of the library.\n\n"
              "To obtain a commercial license or discuss your licensing options, please \n"
              "contact our sales team at https://borb-pdf.com. We value your \n"
              "support and contributions to our library, and we hope to continue providing \n"
              "you with excellent features and support.\n\n"
              "Thank you for your attention and understanding.\n\u001b[0m")
        # fmt: on

    @staticmethod
    def _get_machine_id() -> typing.Optional[str]:
        return MachineID.get()

    @staticmethod
    def _get_user_id() -> str:
        return License.get_user_id() or PersistentRandomUserID.get()

    @staticmethod
    def _send_usage_statistics_in_thread(
        document: typing.Optional["Document"] = None,
        event: str = "",
    ) -> None:  # type: ignore[name-defined]
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
    def send_usage_statistics(
        document: typing.Optional["Document"] = None,
        event: str = "",
    ) -> None:  # type: ignore[name-defined]
        """
        This method sends the usage statistics to the borb license server
        :param event:       the event that is to be registered
        :param document     the Document being processed
        :return:        None
        """

        # easy exit
        if not UsageStatistics._ENABLED:
            return

        # update FAIR_USE counters
        now_in_ms: int = int(time.time() * 1000)
        delta_in_ms: int = (
            now_in_ms - UsageStatistics._FAIR_USE_LAST_INVOCATION_TIMESTAMP_IN_MS
        )
        if (
            delta_in_ms
            > (1000 * 60)
            / UsageStatistics._FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE
        ):
            UsageStatistics._FAIR_USE_LAST_INVOCATION_TIMESTAMP_IN_MS = now_in_ms
            UsageStatistics._FAIR_USE_LAST_INVOCATION_NUMBER_OF_DOCUMENTS = 1
        else:
            UsageStatistics._FAIR_USE_LAST_INVOCATION_TIMESTAMP_IN_MS = now_in_ms
            UsageStatistics._FAIR_USE_LAST_INVOCATION_NUMBER_OF_DOCUMENTS += 1

        # notification
        if (
            UsageStatistics._FAIR_USE_LAST_INVOCATION_NUMBER_OF_DOCUMENTS
            >= UsageStatistics._FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE
        ):
            UsageStatistics._display_fair_use_warning()

        # send in Thread
        try:
            threading.Thread(
                target=UsageStatistics._send_usage_statistics_in_thread,
                args=(document, event),
            ).start()
        except:
            pass
