#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley.
# Modified by Russ Housley to include the opentypemap manager.
#
# Copyright (c) 2021-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# Algorithm Identifiers for AES-GMAC
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc9044.txt
#

from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import univ

from pyasn1_alt_modules import rfc5280
from pyasn1_alt_modules import opentypemap

algorithmIdentifierMap = opentypemap.get('algorithmIdentifierMap')

smimeCapabilityMap = opentypemap.get('smimeCapabilityMap')

# Object Identifiers

aes = univ.ObjectIdentifier((2, 16, 840, 1, 101, 3, 4, 1))

id_aes128_GMAC = aes + (9, )
    
id_aes192_GMAC = aes + (29, )

id_aes256_GMAC = aes + (49, )


# GMAC Parameters

class MACLength(univ.Integer):
    subtypeSpec = constraint.ValueRangeConstraint(12, 16)

class GCMParameters(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('nonce', univ.OctetString()),
        # The nonce may have any number of bits between 8 and 2^64,
        # but it MUST be a multiple of 8 bits. Within the scope of any
        # content-authenticated-encryption key, the nonce value MUST be
        # unique.  A nonce value of 12 octets can be processed more
        # efficiently, so that length is RECOMMENDED.
        namedtype.DefaultedNamedType('length', MACLength().subtype(value=12))
    )


# GMAC Algorithm Identifiers

maca_aes128_GMAC = rfc5280.AlgorithmIdentifier()
maca_aes128_GMAC['algorithm'] = id_aes128_GMAC
# maca_aes128_GMAC['parameters'] are absent

maca_aes192_GMAC = rfc5280.AlgorithmIdentifier()
maca_aes192_GMAC['algorithm'] = id_aes192_GMAC
# maca_aes192_GMAC['parameters'] are absent

maca_aes256_GMAC = rfc5280.AlgorithmIdentifier()
maca_aes256_GMAC['algorithm'] = id_aes256_GMAC
# maca_aes256_GMAC['parameters'] are absent


# Update the Algorithm Identifiers Map and the SMIMECapability Map

_algorithmIdentifierMapUpdate = {
    id_aes128_GMAC: GCMParameters(),
    id_aes192_GMAC: GCMParameters(),
    id_aes256_GMAC: GCMParameters(),
}

algorithmIdentifierMap.update(_algorithmIdentifierMapUpdate)

smimeCapabilityMap.update(_algorithmIdentifierMapUpdate)
