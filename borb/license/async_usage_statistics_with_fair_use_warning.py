#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This implementation of AsyncUsageStatistics tracks the amount of PDF documents
processed and displays a warning (related to the usage of borb, and its dual license)
when the user goes over a certain quota (number of PDF documents processed per minute)
"""
import time
import typing

from borb.license.async_usage_statistics import AsyncUsageStatistics
from borb.license.license import License


class AsyncUsageStatisticsWithFairUseWarning(AsyncUsageStatistics):
    """
    This implementation of AsyncUsageStatistics tracks the amount of PDF documents
    processed and displays a warning (related to the usage of borb, and its dual license)
    when the user goes over a certain quota (number of PDF documents processed per minute)
    """

    _BUCKET_LENGTH_IN_MS: int = 60 * 1000
    _BUCKET_START_IN_MS: int = 0
    _MAX_NUMBER_OF_DOCUMENTS_PER_BUCKET: int = 100
    _NUMBER_OF_DOCUMENTS: int = 0

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

        # reset counter
        AsyncUsageStatisticsWithFairUseWarning._NUMBER_OF_DOCUMENTS = 0

        # display
        # fmt: off
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

    #
    # PUBLIC
    #

    @staticmethod
    def send_usage_statistics(event_name: str = "", document: typing.Optional["Document"] = None) -> None:  # type: ignore[name-defined]
        """
        This method sends (anonymous) usage statistics to the borb server(s)
        :param event_name:  the name of the event (e.g. "PDF.dumps")
        :param document:    the document to which the event is applied
        :return:            None
        """

        # check
        if not AsyncUsageStatistics._ENABLED:
            return

        # call super
        AsyncUsageStatistics.send_usage_statistics(
            event_name=event_name, document=document
        )

        # update FAIR_USE counters
        # 1. calculate delta
        # fmt: off
        now_in_ms: int = int(time.time() * 1000)
        delta_in_ms: int = now_in_ms - AsyncUsageStatisticsWithFairUseWarning._BUCKET_START_IN_MS
        # fmt: on

        # update bucket
        if delta_in_ms < AsyncUsageStatisticsWithFairUseWarning._BUCKET_LENGTH_IN_MS:
            AsyncUsageStatisticsWithFairUseWarning._NUMBER_OF_DOCUMENTS += 1
        else:
            AsyncUsageStatisticsWithFairUseWarning._BUCKET_START_IN_MS = int(
                time.time() * 1000
            )
            AsyncUsageStatisticsWithFairUseWarning._NUMBER_OF_DOCUMENTS = 1

        # IF the user has exceeded the number of documents we consider "fair use"
        # THEN display a notification
        if (
            AsyncUsageStatisticsWithFairUseWarning._NUMBER_OF_DOCUMENTS
            > AsyncUsageStatisticsWithFairUseWarning._MAX_NUMBER_OF_DOCUMENTS_PER_BUCKET
        ):
            AsyncUsageStatisticsWithFairUseWarning._display_fair_use_warning()
