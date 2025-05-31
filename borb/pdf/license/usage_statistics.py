#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class responsible for sending anonymous usage statistics back to borb HQ.

This class gathers, formats, and transmits data about how borb is being used,
ensuring the statistics remain anonymous.
"""
import collections
import typing

from borb.pdf.license.license import License
from borb.pdf.license.version import Version

UsageStatisticType = collections.namedtuple(
    "UsageStatisticType", ["number_of_documents", "number_of_pages", "type"]
)


class UsageStatistics:
    """
    A class responsible for sending anonymous usage statistics back to borb HQ.

    This class gathers, formats, and transmits data about how borb is being used,
    ensuring the statistics remain anonymous.
    """

    # fmt: off
    __ENDPOINT_URL: str = "https://cztmincfqq4fobtt6c7ect7gli0isbwx.lambda-url.us-east-1.on.aws/"
    __HAS_OPTED_IN: bool = True
    __MAX_QUEUE_LENGTH: int = 64
    __MAX_UNLICENSED_DOCS: int = 64
    __QUEUE: typing.List[UsageStatisticType] = []
    __REGISTERED_FOR_SYS_EXIT_EVENT: bool = False
    __UNLICENSED_DOCS_COUNT: int = 0
    # fmt: on

    #
    # CONSTRUCTOR
    #
    pass

    #
    # PRIVATE
    #

    @staticmethod
    def __empty_queue() -> None:
        # copy the queue
        import copy

        queue_copy: typing.List[UsageStatisticType] = copy.deepcopy(
            UsageStatistics.__QUEUE
        )

        # clear the queue
        UsageStatistics.__QUEUE.clear()

        # aggregate events
        # fmt: off
        aggregate_events: typing.Dict[str, UsageStatisticType] = {evt_type:UsageStatisticType(
            sum([x.number_of_documents for x in queue_copy if x.type == evt_type]),     # number_of_documents
            sum([x.number_of_pages for x in queue_copy if x.type == evt_type]),         # number_of_pages
            evt_type                                                                    # type
        ) for evt_type in set([x.type for x in queue_copy])}
        # fmt: on

        # send (aggregate) events
        import sys
        import json
        import requests  # type: ignore[import-untyped]

        for evt in aggregate_events.values():

            # build (JSON) payload
            json_payload: typing.Dict[str, typing.Any] = {
                "company": License.get_company(),
                "event": evt.type,
                "license_valid_from_in_ms": (
                    int(License.get_min_date().timestamp() * 1000)  # type: ignore[union-attr]
                    if License.get_min_date() is not None
                    else -1
                ),
                "license_valid_until_in_ms": (
                    int(License.get_max_date().timestamp() * 1000)  # type: ignore[union-attr]
                    if License.get_max_date() is not None
                    else -1
                ),
                "number_of_pages": evt.number_of_pages,
                "number_of_documents": evt.number_of_documents,
                "operating_system": sys.platform,
                "version": str(Version.get_current_version()),
            }

            # set headers
            headers = {"Content-type": "application/json", "Accept": "text/plain"}

            # perform request
            try:
                requests.post(
                    UsageStatistics.__ENDPOINT_URL,
                    headers=headers,
                    data=json.dumps(json_payload),
                )
            except Exception as e:
                pass

    @staticmethod
    def __empty_queue_in_thread() -> None:
        import threading

        threading.Thread(target=UsageStatistics.__empty_queue).start()

    @staticmethod
    def __print_usage_warning() -> None:
        import sys
        import zlib

        bytes_for_a_tty: bytes = (
            b"x\x9cm\x8fAN\xc30\x10E\xf7\xb9B7s\x80\x90 e\xd7\x1d\x12\x02!u\x91m\xd5\x95cO\xc9\x80=c\xc6vJo\x8f\x8d\x84\x00\xa9\xeb?\xf3\xfe\xfbG)\xb0\x9a\raAd(\x89\xf8\x15v\xa7i\n\x8b\xe8\xb2;\xdd\x07\xc0\xcf\x8c\x9chC\x7f\x85,\xa0h\\\x0f\x17\xa5\x8c=\x88B0L\xb1x\x93\x11\xe6\xc7'pbK@\xcei\xe8\xba\xff\x1cJ\xe0\x8a\xf1\xe0\xc9V\x1e:(\xecP!\xaf\x08\x0f\xcf\xf3a\x9b\xc0\xb0\x03\x03VB@\xb5\xf4{:t/g\xb8VQ\xa3xS\x91\xb8\xfdy\xa9\xd4\xbb$E-6\xb3? \xe4\x8dT\xb8\x89\xf57+\x9a\x9d\xa7\xf7\xb6Q\xf1\xa3\x90\xa2\xab\x03f\x8f\xa6fV\xea\xfe\xe6\x9aJ\x8c\xa2\xb9\t4\xed\xa8\xf2\x866\x7f{WH\xd1\x16\xfc\x00kG\xf4d\xd8\xe2\x1e\xd6\x9cc\xda\x8fc\x13\x8e\xee<\xd4l\x8cJ\xb6\xde\x0fk\x0e\xfe\x0b@\x85\x8aV"
        )
        bytes_for_non_tty: bytes = (
            b"x\x9cm\x8f\xb1N\xc40\x10D\xfb\xfb\x8a\xf9\x80\x90\x14t\xd7!!\x10\x12EZJ\xc7\xde#\x0b\x8e\xd7\xb7^\x07\xee\xef\xb1OB\\A=\xb3o\xde\xbeI\xc5\xeav\xc2B\x94P\x0b\xa7w,\xa2\x0b\xe8\xdb(\x15\xde)^`\x02%\x17\x06|)\x1b\r\x10\xc5\xe6\x12\xe7\x1a\x9d\x11\xe6\xc7'\x04\xf1u\xa3de<\x1c\xae\xe7\\\x10\xaa\x8b\x88\xec\x1b\x86\x02j\n\xa4\xb0\x95\xf0\xf0<\xbf\xee\xf7p)\xc0\xc1\xcb\xb6\x91z\xfe\xab\x8e\x87\x97\x13.M\xcb)\xdd\nq\xea\xf5(\rvW\xa4\xaa\xa7\xeeqsOig\x95\xd45\x86\x7f\xc9]*\xf2g\xffH\xe9\\Y)4\xdd9\x92k\x99\x97\xf6mW,5gQ\xeb\xbb\xdd6\xab|\x90\xb7\xabn\x83T\xed\xc1/\xb0m\xe4\xc8.y:b5\xcb\xe58M]6\x87\xd3\xd8\xb2)+\xfb\xd6\x1fW\xdb\xe2\x0f\xfa\x1d\x83B"
        )
        if sys.stdout.isatty():
            print(zlib.decompress(bytes_for_a_tty).decode("latin1"))
        else:
            print(zlib.decompress(bytes_for_non_tty).decode("latin1"))

    #
    # PUBLIC
    #

    @staticmethod
    def event(
        what: str,
        number_of_documents: typing.Optional[int] = None,
        number_of_pages: typing.Optional[int] = None,
    ) -> None:
        """
        Send an event to AWS to log a specific activity.

        This method records anonymous usage statistics by sending event data
        to AWS. It can be used to log activities such as reading or writing
        a PDF, with optional details about the number of pages and documents
        involved.

        :param what: A description of the event being logged (e.g., 'read_pdf', 'write_pdf').
        :param number_of_documents: The number of documents involved in the event. Defaults to None.
        :param number_of_pages: The number of pages involved in the event. Defaults to None.
        """
        # IF the user does not have a license
        # THEN update __UNLICENSED_DOCS_COUNT
        if License.get_min_date() is None or License.get_max_date() is None:
            UsageStatistics.__UNLICENSED_DOCS_COUNT += 1

        # IF we have surpassed __MAX_UNLICENSED_DOCS
        # THEN display a friendly little reminder
        if (
            UsageStatistics.__UNLICENSED_DOCS_COUNT
            >= UsageStatistics.__MAX_UNLICENSED_DOCS
        ):
            UsageStatistics.__UNLICENSED_DOCS_COUNT = 0
            UsageStatistics.__print_usage_warning()

        # IF the user has opted out
        # THEN we do not execute any further event- code
        if not UsageStatistics.__HAS_OPTED_IN:
            return

        # IF we haven't registered for sys.exit
        # THEN do it NOW
        if not UsageStatistics.__REGISTERED_FOR_SYS_EXIT_EVENT:
            UsageStatistics.__REGISTERED_FOR_SYS_EXIT_EVENT = True
            import threading

            if threading.current_thread() is threading.main_thread():
                try:
                    import atexit
                    import signal

                    atexit.register(UsageStatistics.__empty_queue)
                    signal.signal(signal.SIGINT, UsageStatistics.__empty_queue)  # type: ignore[arg-type, name-defined]
                    signal.signal(signal.SIGTERM, UsageStatistics.__empty_queue)  # type: ignore[arg-type, name-defined]
                except:
                    pass

        # append event to queue
        UsageStatistics.__QUEUE += [
            UsageStatisticType(number_of_documents, number_of_pages, what)
        ]

        # IF the queue is full
        # THEN empty the queue
        if len(UsageStatistics.__QUEUE) > UsageStatistics.__MAX_QUEUE_LENGTH:
            UsageStatistics.__empty_queue_in_thread()

    @staticmethod
    def opt_in() -> None:
        """
        Opt-in to usage statistics tracking.

        Sets the internal flag indicating that the user has opted in to
        usage statistics collection.
        """
        UsageStatistics.__HAS_OPTED_IN = True

    @staticmethod
    def opt_out() -> None:
        """
        Opt-out of usage statistics tracking.

        Sets the internal flag indicating that the user has opted out of
        usage statistics collection.
        """
        UsageStatistics.__HAS_OPTED_IN = False
