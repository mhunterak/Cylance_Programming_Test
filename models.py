from datetime import datetime as dt
from datetime import timedelta as td
import json
import uuid

import peewee

from config import DEBUG

if DEBUG:
    DATABASE = peewee.SqliteDatabase('GUID_test.db')
else:
    DATABASE = peewee.SqliteDatabase('GUID.db')  # pragma: no cover


def Set_GUID():
    ''' If a GUID is not provided, this function will generate a new one '''
    return uuid.uuid4().hex.upper()


def validate_GUID(input):
    '''
    Validates GUID input. returns True for valid input
    '''
    # must be 32 characters
    if len(input) != 32:
        return False
    # must use uppercase letters
    elif input != input.upper():
        return False
    # must be alphanumeric
    elif not input.isalnum():
        return False
    # if tests pass, return true
    else:
        return True


def Set_Expiration():
    ''' This function is used in creating the default expiration date '''
    return Unix_from_datetime(dt.now()+td(days=30))


def Unix_from_datetime(inputDatetime):
    ''' Generates a unix timestamp from a Python datetime '''
    return int(dt.timestamp(inputDatetime))


class MdObj(peewee.Model):
    '''
    The MdObj model (short for Metadata Object) holds the GUID of each object in
    the database, to "maintain a database of GUIDs (Globally Unique Identifier)
    and associated metadata"

    no explicit fields for metadata have been added, but the base model is here
    '''
    guid = peewee.CharField(
        max_length=32,
        default=Set_GUID
    )
    expire = peewee.DateTimeField(
        default=Set_Expiration
    )
    user = peewee.CharField(
        # a user is always required
        max_length=32
    )

    class Meta:
        database = DATABASE


def initialize():
    '''
    Initializes the database
    '''
    # connect to the DATABASE
    DATABASE.connect(reuse_if_open=True)
    # build the tables for MdObj in the DATABASE
    DATABASE.create_tables([MdObj], safe=True)
    # close the DATABASE connection
    DATABASE.close()
