#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley with some assistance from asn1ate v.0.6.0.
# Modified by Russ Housley to include the opentypemap manager.
#
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# Transport Layer Security (TLS) Feature Certificate Extension
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc7633.txt
#

from pyasn1.type import univ

from pyasn1_alt_modules import opentypemap

certificateExtensionsMap = opentypemap.get('certificateExtensionsMap')


# TLS Features Extension

id_pe = univ.ObjectIdentifier('1.3.6.1.5.5.7.1')

id_pe_tlsfeature = id_pe + (24, )


class Features(univ.SequenceOf):
    componentType = univ.Integer()


# Update the Certificate Extensions Map

_certificateExtensionsMapUpdate = {
    id_pe_tlsfeature: Features(),
}

certificateExtensionsMap.update(_certificateExtensionsMapUpdate)
