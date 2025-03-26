#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley.
# Modified by Russ Housley to include the opentypemap manager.
#
# Copyright (c) 2021-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# S/MIME Capabilities Certificate Extension
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc4262.txt
#

from pyasn1_alt_modules import rfc5751
from pyasn1_alt_modules import opentypemap

certificateExtensionsMap = opentypemap.get('certificateExtensionsMap')


# Imports from RFC 5751

smimeCapabilities = rfc5751.smimeCapabilities

SMIMECapabilities = rfc5751.SMIMECapabilities

SMIMECapability = rfc5751.SMIMECapability


# Update the Certificate Extensions Map

_certificateExtensionsMap = {
    smimeCapabilities: SMIMECapabilities(),
}

certificateExtensionsMap.update(_certificateExtensionsMap)
