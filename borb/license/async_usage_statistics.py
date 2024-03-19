#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class implements the basics for sending usage statistics to the borb server(s).
These kinds of checks are useful to get an idea of which functionality is most often used,
where development effort needs to be spent, etc
"""
import atexit
import json
import signal
import sys
import threading
import time
import typing
from decimal import Decimal

import requests

from borb.license.license import License
from borb.license.persistent_random_user_id import PersistentRandomUserID
from borb.license.version import Version


class AsyncUsageStatistics:
    """
    This class implements the basics for sending usage statistics to the borb server(s).
    These kinds of checks are useful to get an idea of which functionality is most often used,
    where development effort needs to be spent, etc
    """

    class Event:
        """
        This class represents something that happened that needs to be sent to the borb server(s).
        """

        def __init__(
            self,
            count: int,
            event_name: str,
            number_of_pages: int,
        ):
            self._count: int = count
            self._creation_timestamp_in_ms: int = int(time.time() * 1000)
            self._event_name: str = event_name
            self._number_of_pages: typing.List[int] = [number_of_pages]

        def get_avg_number_of_pages(self) -> int:
            """
            This function returns the average number of pages in this Event.
            e.g.    2 PDF documents have been read, one of 10 pages and one of 2 pages.
                    This function would return 6.
            :return:    the average number of pages in this Event
            """
            if len(self._number_of_pages) == 0:
                return 0
            return sum(self._number_of_pages) // len(self._number_of_pages)

        def get_max_number_of_pages(self) -> int:
            """
            This function returns the maximum number of pages in this Event.
            e.g.    2 PDF documents have been read, one of 10 pages and one of 2 pages.
                    This function would return 10.
            :return:    the maximum number of pages in this Event
            """
            if len(self._number_of_pages) == 0:
                return 0
            return max(self._number_of_pages)

        def get_min_number_of_pages(self) -> int:
            """
            This function returns the minimum number of pages in this Event.
            e.g.    2 PDF documents have been read, one of 10 pages and one of 2 pages.
                    This function would return 2.
            :return:    the minimum number of pages in this Event
            """
            if len(self._number_of_pages) == 0:
                return 0
            return min(self._number_of_pages)

    # fmt: off
    _ENABLED: bool = True
    _ENDPOINT_URL: str = "https://cztmincfqq4fobtt6c7ect7gli0isbwx.lambda-url.us-east-1.on.aws/"
    _EVENT_QUEUE: typing.List[Event] = []
    _MAX_NUMBER_OF_MS_BETWEEN_SENDING: int = 5 * 1000
    _REGISTERED_FOR_SYS_EXIT_EVENT: bool = False
    # fmt: on

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def _get_number_of_pages(document: typing.Optional["Document"]) -> int:  # type: ignore[name-defined]
        if document is None:
            return 0
        return int(document.get_document_info().get_number_of_pages() or Decimal(0))

    @staticmethod
    def _get_user_id() -> typing.Optional[str]:
        return License.get_user_id() or PersistentRandomUserID.get()

    @staticmethod
    def _process_event_queue() -> None:

        # easy exit
        if not AsyncUsageStatistics._ENABLED:
            return

        # copy _EVENT_QUEUE
        # this ensures that if this code gets executed concurrently, the queue is empty
        # fmt: off
        queue_copy: typing.List[AsyncUsageStatistics.Event] = AsyncUsageStatistics._EVENT_QUEUE
        # fmt: on

        # clear _EVENT_QUEUE
        AsyncUsageStatistics._EVENT_QUEUE = []

        # process _EVENT_QUEUE
        for evt in queue_copy:

            # build JSON payload
            json_payload: typing.Dict[str, typing.Any] = {
                "anonymous_user_id": AsyncUsageStatistics._get_user_id(),
                "company": License.get_company(),
                "count": evt._count,
                "event": evt._event_name,
                "license_valid_from_in_ms": License.get_valid_from_in_ms(),
                "license_valid_until_in_ms": License.get_valid_until_in_ms(),
                "number_of_pages": evt.get_avg_number_of_pages(),
                "min_number_of_pages": evt.get_min_number_of_pages(),
                "max_number_of_pages": evt.get_max_number_of_pages(),
                "sys_platform": sys.platform,
                "utc_time_in_ms": int(time.time() * 1000),
                "version": Version.get_version(),
            }

            # set headers
            headers = {"Content-type": "application/json", "Accept": "text/plain"}

            # perform request
            try:
                requests.post(
                    AsyncUsageStatistics._ENDPOINT_URL,
                    headers=headers,
                    data=json.dumps(json_payload),
                )
            except Exception as e:
                pass

    @staticmethod
    def _send_usage_statistics_immediately() -> None:

        # easy exit
        if not AsyncUsageStatistics._ENABLED:
            return

        # easy exit
        if len(AsyncUsageStatistics._EVENT_QUEUE) == 0:
            return

        # IF the earliest event is less than 5 seconds ago
        # THEN return
        now_in_ms: int = int(time.time() * 1000)
        delta_in_ms: int = now_in_ms - min(
            [x._creation_timestamp_in_ms for x in AsyncUsageStatistics._EVENT_QUEUE]
        )
        if delta_in_ms < AsyncUsageStatistics._MAX_NUMBER_OF_MS_BETWEEN_SENDING:
            return

        # process _EVENT_QUEUE in Thread
        try:
            threading.Thread(
                target=AsyncUsageStatistics._process_event_queue,
            ).start()
        except Exception as e:
            AsyncUsageStatistics._ENABLED = False
            return

    #
    # PUBLIC
    #

    @staticmethod
    def disable() -> None:
        """
        This function disables the sending of usage statistics
        :return:    None
        """
        AsyncUsageStatistics._ENABLED = False

    @staticmethod
    def enable() -> None:
        """
        This function enables the sending of usage statistics
        :return:    None
        """
        AsyncUsageStatistics._ENABLED = True

    @staticmethod
    def send_usage_statistics(event_name: str = "", document: typing.Optional["Document"] = None) -> None:  # type: ignore[name-defined]
        """
        This method sends (anonymous) usage statistics to the borb server
        :param event_name:  the name of the event (e.g. "PDF.dumps")
        :param document:    the document to which the event is applied
        :return:            None
        """

        # easy exit
        if not AsyncUsageStatistics._ENABLED:
            return

        # IF we haven't registered for sys.exit
        # THEN do it NOW
        if not AsyncUsageStatistics._REGISTERED_FOR_SYS_EXIT_EVENT:
            AsyncUsageStatistics._REGISTERED_FOR_SYS_EXIT_EVENT = True
            if threading.current_thread() is threading.main_thread():
                atexit.register(AsyncUsageStatistics._process_event_queue)
                signal.signal(signal.SIGINT, AsyncUsageStatistics._process_event_queue)  # type: ignore[arg-type]
                signal.signal(signal.SIGTERM, AsyncUsageStatistics._process_event_queue)  # type: ignore[arg-type]

        # IF no existing Event matches the event_name
        # THEN create a new Event
        number_of_pages: int = AsyncUsageStatistics._get_number_of_pages(document)
        if len(AsyncUsageStatistics._EVENT_QUEUE) == 0 or not any(
            [x._event_name == event_name for x in AsyncUsageStatistics._EVENT_QUEUE]
        ):
            AsyncUsageStatistics._EVENT_QUEUE.append(
                AsyncUsageStatistics.Event(
                    count=1,
                    event_name=event_name,
                    number_of_pages=number_of_pages,
                )
            )
            AsyncUsageStatistics._send_usage_statistics_immediately()
            return

        # IF a matching Event exists
        # THEN update the existing Event (count, number_of_pages)
        try:
            for i in range(0, len(AsyncUsageStatistics._EVENT_QUEUE)):
                if AsyncUsageStatistics._EVENT_QUEUE[i]._event_name == event_name:
                    AsyncUsageStatistics._EVENT_QUEUE[i]._count += 1
                    AsyncUsageStatistics._EVENT_QUEUE[i]._number_of_pages.append(
                        number_of_pages
                    )
                    break
        except:
            pass

        #
        AsyncUsageStatistics._send_usage_statistics_immediately()
