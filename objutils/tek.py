#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.1.0"

__copyright__ = """
    pyObjUtils - Object file library for Python.

   (C) 2010-2016 by Christoph Schueler <cpu12.gems@googlemail.com>

   All Rights Reserved

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import objutils.hexfile as hexfile
import objutils.utils as utils
import objutils.checksums as checksums

DATA    = 1
EOF     = 2

class Reader(hexfile.Reader):

    FORMAT_SPEC = (
        (DATA,  "/AAAALLBBDDCC"),
        (EOF,   "/AAAA00BB"),
    )

    def checkLine(self, line, formatType):
        if formatType == DATA:
            if line.length != len(line.chunk):
                raise hexfile.InvalidRecordLengthError("Byte count doesn't match length of actual data.")
            addrChecksum = 0
            addressChecksum = checksums.nibbleSum(utils.makeList(utils.intToArray(line.address), line.length))
            if line.addrChecksum != addressChecksum:
                raise hexfile.InvalidRecordChecksumError()
            checksum = checksums.nibbleSum(line.chunk)
            if line.checksum != checksum:
                raise hexfile.InvalidRecordChecksumError()

    def isDataLine(self, line, formatType):
        return formatType == DATA


class Writer(hexfile.Writer):

    MAX_ADDRESS_BITS = 16


    def composeFooter(self, meta):
        return "/{0:04X}00{1:02X}".format(self.lastAddress, checksums.nibbleSum(utils.intToArray(self.lastAddress)))

    def composeRow(self, address, length, row):
        addressChecksum = checksums.nibbleSum(utils.makeList(utils.intToArray(address), length))

        dataChecksum = checksums.nibbleSum(row)
        line = "/{0:04X}{1:02X}{2:02X}{3!s}{4:02X}".format(address, length, addressChecksum, Writer.hexBytes(row), dataChecksum)
        self.lastAddress = address + length
        return line

