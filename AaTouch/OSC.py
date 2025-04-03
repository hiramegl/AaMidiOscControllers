#!/usr/bin/python
#
# Open SoundControl for Python
# Copyright (C) 2002 Daniel Holth, Clinton McChesney
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For questions regarding this module contact
# Daniel Holth <dholth@stetson.edu> or visit
# http://www.stetson.edu/~ProctoLogic/
#
# Changelog:
# 15 Nov. 2001:
#   Removed dependency on Python 2.0 features.
#   - dwh
# 13 Feb. 2002:
#   Added a generic callback handler.
#   - dwh
#
# Updated June 2007 by Hans Huebner (hans.huebner@gmail.com)
#   Improved bundle support, API cleanup

import sys
import struct
import math
import string

import Live

# OSC Message **********************************************

class OSCMessage:
    """Builds typetagged OSC messages."""

    def __init__(self):
        self.address  = ""
        self.typetags = b","
        self.message  = bytearray()

    def setAddress(self, address):
        self.address = address

    def setTypetags(self, typetags):
        self.typetags = typetags.encode('ascii')

    def setMessage(self, message):
        self.message = message.encode('ascii')

    def clear(self):
        self.address  = ""
        self.clearData()

    def clearData(self):
        self.typetags = b","
        self.message  = bytearray()

    def append(self, argument, typehint = None):
        """Appends data to the message,
        updating the typetags based on
        the argument's type.
        If the argument is a blob (counted string)
        pass in 'b' as typehint."""

        if typehint == 'b':
            binary = OSCBlob(argument)
        else:
            binary = OSCArgument(argument)

        self.typetags = self.typetags + binary[0]
        self.rawAppend(binary[1])

    def rawAppend(self, data):
        """Appends raw data to the message.  Use append()."""
        self.message = self.message + data

    def getBinary(self):
        """Returns the binary message (so far) with typetags."""
        address  = OSCArgument(self.address)[1]
        typetags = OSCArgument(self.typetags.decode('ascii'))[1]
        return address + typetags + self.message

    def __repr__(self):
        return self.getBinary()

# OSC Bundle ***********************************************

JAN_1970      = 2208988800
SECS_TO_PICOS = 4294967296

def abs_to_timestamp(abs):
    """ since 1970 => since 1900 64b OSC """
    sec_1970 = long(abs)
    sec_1900 = sec_1970 + JAN_1970

    sec_frac = float(abs - sec_1970)
    picos = long(sec_frac * SECS_TO_PICOS)

    total_picos = (abs + JAN_1970) * SECS_TO_PICOS
    return struct.pack('!LL', sec_1900, picos)


class OSCBundle:
    """Builds OSC bundles"""
    def __init__(self, when=None):
        self.items = []
        if when == None:
            when = time.time()
        self.when = when

    def append(self, address, msg = None):
        if isinstance(address, str):
            self.items.append(OSCMessage(address, msg))
        elif isinstance(address, OSCMessage):
            # address really is an OSCMessage
            self.items.append(address)
        else:
            raise Exception('invalid type of first argument to OSCBundle.append(), need address string or OSCMessage, not ', str(type(address)))

    def getBinary(self):
        retval = OSCArgument('#bundle')[1] + abs_to_timestamp(self.when)
        for item in self.items:
            binary = item.getBinary()
            retval = retval + OSCArgument(len(binary))[1] + binary
        return retval


# auxiliar methods *****************************************

def readString(data):
    length   = data.find(0)
    nextData = int(math.ceil((length + 1) / 4.0) * 4)
    return (data[0:length].decode('ascii'), data[nextData:])


def readBlob(data):
    length   = struct.unpack(">i", data[0:4])[0]
    nextData = int(math.ceil((length) / 4.0) * 4) + 4
    return (data[4:length+4], data[nextData:])


def readInt(data):
    if(len(data)<4):
        print("Error: too few bytes for int", data, len(data))
        rest = data
        integer = 0
    else:
        integer = int(struct.unpack(">i", data[0:4])[0])
        rest    = data[4:]
    return (integer, rest)


def readLong(data):
    """Tries to interpret the next 8 bytes of the data
    as a 64-bit signed integer."""
    high = struct.unpack(">i", data[0:4])[0]
    data = data[4:]
    low  = struct.unpack(">i", data[0:4])[0]
    big = (high << 32) + low
    rest = data[4:]
    return (big, rest)


def readFloat(data):
    if(len(data) < 4):
        print("Error: too few bytes for float", data, len(data))
        float_num = 0
        rest      = data
    else:
        float_num = struct.unpack(">f", data[0:4])[0]
        rest      = data[4:]

    return (float_num, rest)


def OSCBlob(next):
    """Convert a string into an OSC Blob,
    returning a (typetag, data) tuple."""

    if type(next) == type(b"binary"):
        length = len(next)
        padded = math.ceil((len(next)) / 4.0) * 4
        binary = struct.pack(">i%ds" % (padded), length, next)
        tag    = b'b'
    else:
        tag    = bytearray()
        binary = bytearray()

    return (tag, binary)


def OSCArgument(next):
    """Convert some Python types to their
    OSC binary representations, returning a
    (typetag, data) tuple."""

    if type(next) == type(""):
        strLen = math.ceil((len(next)+1) / 4.0) * 4
        binary = struct.pack(">%ds" % (strLen), next.encode('ascii'))
        tag    = b"s"
    elif type(next) == type(42.5):
        binary = struct.pack(">f", next)
        tag    = b"f"
    elif type(next) == type(13):
        binary = struct.pack(">i", next)
        tag    = b"i"
    else:
        binary = bytearray()
        tag    = bytearray()

    return (tag, binary)


def parseArgs(args):
    """Given a list of strings, produces a list
    where those strings have been parsed (where
    possible) as floats or integers."""
    parsed = []
    for arg in args:
        print(arg)
        arg = arg.strip()
        interpretation = None
        try:
            interpretation = float(arg)
            if string.find(arg, ".") == -1:
                interpretation = int(interpretation)
        except:
            # Oh - it was a string.
            interpretation = arg
            pass
        parsed.append(interpretation)
    return parsed


def decodeOSC(data):
    """Converts a typetagged OSC message to a Python list."""
    table = {"i":readInt, "f":readFloat, "s":readString, "b":readBlob}
    decoded = []
    address, rest = readString(data)
    typetags = ""

    if address == "#bundle":
        time, rest = readLong(rest)
        decoded.append(address)
        decoded.append(time)
        while len(rest)>0:
            length, rest = readInt(rest)
            decoded.append(decodeOSC(rest[:length]))
            rest = rest[length:]
    elif len(rest) > 0:
        typetags, rest = readString(rest)
        decoded.append(address)
        decoded.append(typetags)
        if(typetags[0] == ","):
            for tag in typetags[1:]:
                value, rest = table[tag](rest)
                decoded.append(value)
        else:
            print("Oops, typetag lacks the magic ,")

    # return only the data
    return decoded


# Callback Manager *****************************************

class CallbackManager:
    """This utility class maps OSC addresses to callables.

    The CallbackManager calls its callbacks with a list
    of decoded OSC arguments, including the address and
    the typetags as the first two arguments."""

    def __init__(self):
        self.callbacks = {}
        self.add(self.unbundler, "#bundle")


    def handle(self, data, source = None):
        """Given OSC data, tries to call the callback with the
        right address."""
        decoded = decodeOSC(data)
        self.dispatch(decoded)


    def dispatch(self, message):
        """Sends decoded OSC data to an appropriate callback"""
        try:
            address = message[0]
            segments = address.split('/')
            self.callbacks[address](segments, message)
        except KeyError as e:
            Live.Base.log("-> Callback not found for address '{0}'. Msg: [{1}]".format(address, message))
            pass
        except None as e:
            Live.Base.log("-> Exception, address: '{0}', callback: [{1}]".format(address, e))

        return


    def add(self, callback, name):
        """Adds a callback to our set of callbacks,
        or removes the callback with name if callback
        is None."""
        if callback == None:
            del self.callbacks[name]
        else:
            self.callbacks[name] = callback


    def unbundler(self, messages):
        """Dispatch the messages in a decoded bundle."""
        # first two elements are #bundle and the time tag, rest are messages.
        for message in messages[2:]:
            self.dispatch(message)

# OSC bundles:
# ------------------------+---------------------------------+--------------------------------------------+
#          DATA           |              SIZE               |                   PURPOSE                  |
# ------------------------+---------------------------------+--------------------------------------------+
# OSC-string "#bundle"    | 8 bytes                         | How to know that this data is a bundle     |
# ------------------------+---------------------------------+--------------------------------------------+
# OSC-timetag             | 8 bytes                         | Time tag that applies to the entire bundle |
# ------------------------+---------------------------------+--------------------------------------------+
# Size of first bundle    | 4 bytes                         |                                            |
# element                 | (int32)                         | First bundle element                       |
# ------------------------+---------------------------------+--------------------------------------------+
# First bundle element's  | As many bytes as given by       |                                            |
# contents                | "size of first bundle element"  |                                            |
# ------------------------+---------------------------------+--------------------------------------------+
# Size of second bundle   | 4 bytes                         |                                            |
# element                 | (int32)                         | Second bundle element                      |
# ------------------------+---------------------------------+--------------------------------------------+
# Second bundle element's | As many bytes as given by       |                                            |
# contents                | "size of second bundle element" |                                            |
# ------------------------+---------------------------------+--------------------------------------------+
