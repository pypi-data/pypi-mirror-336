#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley with assistance from asn1ate v.0.6.0.
#
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# X.509 Certificate Extension for Hash Of Root Key
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc8649.txt
#

from pyasn1.type import namedtype
from pyasn1.type import univ

from pyasn1_alt_modules import rfc5280
from pyasn1_alt_modules import opentypemap

certificateExtensionsMap = opentypemap.get('certificateExtensionsMap')


id_ce_hashOfRootKey = univ.ObjectIdentifier('1.3.6.1.4.1.51483.2.1')


class HashedRootKey(univ.Sequence):
    pass

HashedRootKey.componentType = namedtype.NamedTypes(
    namedtype.NamedType('hashAlg', rfc5280.AlgorithmIdentifier()),
    namedtype.NamedType('hashValue', univ.OctetString())
)


# Update the Certificate Extensions Map

_certificateExtensionsMapUpdate = {
    id_ce_hashOfRootKey: HashedRootKey(),	
}

certificateExtensionsMap.update(_certificateExtensionsMapUpdate)
