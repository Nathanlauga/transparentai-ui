from enum import Enum

from flask_babel import _


class Error(Enum):
    ReadCsvError = 'ReadCsvError'
