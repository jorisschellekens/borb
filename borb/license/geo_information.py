#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class offers a way of looking up the geographic information associated with the IP address
of this system.
"""
import json
import threading
import typing
import urllib.request


class GeoInformation:
    """
    This class offers a way of looking up the geographic information associated with the IP address
    of this system.
    """

    _city: typing.Optional[str] = None
    _country_code: typing.Optional[str] = None
    _country_name: typing.Optional[str] = None
    _is_retrieving: bool = False
    _latitude: typing.Optional[float] = None
    _longitude: typing.Optional[float] = None
    _state: typing.Optional[str] = None

    @staticmethod
    def get_city() -> typing.Optional[str]:
        """
        This function returns the city (e.g. Ghent)
        associated with the IP of this system. If the city still needs to be determined, None is returned.
        :return:    the city
        """
        if (
            GeoInformation._city is None
            and GeoInformation._country_code is None
            and GeoInformation._country_name is None
            and GeoInformation._latitude is None
            and GeoInformation._longitude is None
            and GeoInformation._state is None
        ):
            threading.Thread(target=GeoInformation._get).start()
        return GeoInformation._city

    @staticmethod
    def get_country_code() -> typing.Optional[str]:
        """
        This function returns the country code (e.g. BE)
        associated with the IP of this system. If the country code still needs to be determined, None is returned.
        :return:    the country code
        """
        if (
            GeoInformation._city is None
            and GeoInformation._country_code is None
            and GeoInformation._country_name is None
            and GeoInformation._latitude is None
            and GeoInformation._longitude is None
            and GeoInformation._state is None
        ):
            threading.Thread(target=GeoInformation._get).start()
        return GeoInformation._country_code

    @staticmethod
    def get_country_name() -> typing.Optional[str]:
        """
        This function returns the country name (e.g. Belgium)
        associated with the IP of this system. If the country name still needs to be determined, None is returned.
        :return:    the country name
        """
        if (
            GeoInformation._city is None
            and GeoInformation._country_code is None
            and GeoInformation._country_name is None
            and GeoInformation._latitude is None
            and GeoInformation._longitude is None
            and GeoInformation._state is None
        ):
            threading.Thread(target=GeoInformation._get).start()
        return GeoInformation._country_name

    @staticmethod
    def get_latitude() -> typing.Optional[float]:
        """
        This function returns the latitude (e.g. 51.05)
        associated with the IP of this system. If the latitude still needs to be determined, None is returned.
        :return:    the latitude
        """
        if (
            GeoInformation._city is None
            and GeoInformation._country_code is None
            and GeoInformation._country_name is None
            and GeoInformation._latitude is None
            and GeoInformation._longitude is None
            and GeoInformation._state is None
        ):
            threading.Thread(target=GeoInformation._get).start()
        return GeoInformation._latitude

    @staticmethod
    def get_longitude() -> typing.Optional[float]:
        """
        This function returns the longitude (e.g. 3.71667)
        associated with the IP of this system. If the longitude still needs to be determined, None is returned.
        :return:    the longitude
        """
        if (
            GeoInformation._city is None
            and GeoInformation._country_code is None
            and GeoInformation._country_name is None
            and GeoInformation._latitude is None
            and GeoInformation._longitude is None
            and GeoInformation._state is None
        ):
            threading.Thread(target=GeoInformation._get).start()
        return GeoInformation._longitude

    @staticmethod
    def get_state() -> typing.Optional[str]:
        """
        This function returns the state (e.g. East-Flanders)
        associated with the IP of this system. If the state still needs to be determined, None is returned.
        :return:    the state
        """
        if (
            GeoInformation._city is None
            and GeoInformation._country_code is None
            and GeoInformation._country_name is None
            and GeoInformation._latitude is None
            and GeoInformation._longitude is None
            and GeoInformation._state is None
        ):
            threading.Thread(target=GeoInformation._get).start()
        return GeoInformation._state

    @staticmethod
    def _get():
        # IF we are already busy retrieving the geo information
        # THEN skip
        if GeoInformation._is_retrieving:
            return
        GeoInformation._is_retrieving = True

        # fetch the IP
        ipv4: typing.Optional[str] = None
        try:
            ipv4 = urllib.request.urlopen("https://v4.ident.me").read().decode("utf8")
        except:
            pass
        if ipv4 is None:
            GeoInformation._is_retrieving = False
            return

        # fetch the location
        location_data: typing.Dict[str, str] = {}
        try:
            location_data = json.loads(
                urllib.request.urlopen(
                    "https://geolocation-db.com/json/%s&position=true" % ipv4
                )
                .read()
                .decode("utf8")
            )
        except:
            pass
        if len(location_data) == 0:
            GeoInformation._is_retrieving = False
            return

        GeoInformation._city = location_data.get("city", None)
        GeoInformation._country_code = location_data.get("country_code", None)
        GeoInformation._country_name = location_data.get("country_name", None)
        GeoInformation._latitude = location_data.get("latitude", None)
        GeoInformation._longitude = location_data.get("longitude", None)
        GeoInformation._state = location_data.get("state", None)

        # return
        GeoInformation._is_retrieving = False
