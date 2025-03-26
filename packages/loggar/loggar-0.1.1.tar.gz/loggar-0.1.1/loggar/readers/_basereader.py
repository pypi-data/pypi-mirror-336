#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides the *private* and generalised base
            reader functionality.

Note:
            This module is *not* designed to be interacted with directly,
            but rather to be inherited and specialised by a reader-specific class.

:Platform:  Linux/Windows | Python 3.8+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error
# pylint: disable=wrong-import-order

import pandas as pd
import socket
# locals
from libs.config import systemcfg


class _BaseReader:
    """Private, generalised reader class.

    This class is *not* designed to be interacted with directly, but
    rather inherited and specialised by a reader-specific parent class.

    Args:
        host (str): Hostname.
        ip (str): IP address; used for SSH.
        port (int, optional): SSH port. Defaults to 22.

    """

    _CMD = None
    _ME = socket.gethostname().lower()
    _USER = systemcfg['user']

    def __init__(self, host: str, ip: str, port: int=22):
        """Reader class initialiser."""
        self._host = host
        self._ip = ip
        self._port = str(port)
        self._data = pd.DataFrame()  # Parsed and prep'd log data as a DataFrame.
        self._text = None            # Raw text from the log.

    @property
    def data(self) -> pd.DataFrame:
        """Accessor to the parsed and prepared data as a DataFrame."""
        return self._data

    @data.setter
    def data(self, value: pd.DataFrame):
        """Value setter for the the parsed and prepared data."""
        if not isinstance(value, pd.DataFrame):
            raise ValueError('Invalid type. Expected type: pd.DataFrame.')
        self._data = value

    @property
    def host(self) -> str:
        """Accessor to the hostname."""
        return self._host

    @property
    def text(self) -> str:
        """Accessor to the text captured from the log file."""
        return self._text

    def read(self):
        """Read the relevant log file.

        Once the log is read, the text is stored into the :attr:`_text`
        attribute, for public access via the :attr:`text` property.

        """
        self._read()

    def _read(self):
        """Reader-specific log reader method.

        This is a stub-method designed to be overridden by the child
        class.

        """
