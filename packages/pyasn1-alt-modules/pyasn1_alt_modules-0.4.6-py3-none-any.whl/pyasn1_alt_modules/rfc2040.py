#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley.
# Modified by Russ Housley to include the opentypemap manager and
#   update the S/MIME Capability map.
#
# Copyright (c) 2021-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# Identifiers for RC5
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc2040.txt
# https://www.rfc-editor.org/rfc/rfc8018.txt
#

from pyasn1_alt_modules import rfc5280
from pyasn1_alt_modules import rfc8018
from pyasn1_alt_modules import opentypemap

algorithmIdentifierMap = opentypemap.get('algorithmIdentifierMap')

smimeCapabilityMap = opentypemap.get('smimeCapabilityMap')


# The same RC5 object identifiers are defined in RFC 8018

encryptionAlgorithm = rfc8018.encryptionAlgorithm

rc5_CBC = encryptionAlgorithm + (8, )

rc5_CBC_PAD = rfc8018.rc5_CBC_PAD


# The RC5 CBC parameters are defined in RFC 8018

RC5_CBC_Parameters = rfc8018.RC5_CBC_Parameters


# Update the Algorithm Identifier Map and the S/MIME Capability Map
# for the one not already handled by importing rfc8018.

_algorithmIdentifierMapUpdate = {
    rc5_CBC: RC5_CBC_Parameters(),
}

algorithmIdentifierMap.update(_algorithmIdentifierMapUpdate)

smimeCapabilityMap.update(_algorithmIdentifierMapUpdate)
