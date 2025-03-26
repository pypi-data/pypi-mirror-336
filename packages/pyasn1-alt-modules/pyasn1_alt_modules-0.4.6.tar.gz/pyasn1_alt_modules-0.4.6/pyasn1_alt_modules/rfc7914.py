#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley with assistance from asn1ate v.0.6.0.
# Modified by Russ Housley to include the opentypemap manager.
#
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# The scrypt Password-Based Key Derivation Function
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc8520.txt
# https://www.rfc-editor.org/errata/eid5871
#

from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import univ

from pyasn1_alt_modules import opentypemap

algorithmIdentifierMap = opentypemap.get('algorithmIdentifierMap')

MAX = float('inf')


# Algorithm identifier and parameters for the
# scrypt Password-Based Key Derivation Function

id_scrypt = univ.ObjectIdentifier('1.3.6.1.4.1.11591.4.11')


class Scrypt_params(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('salt',
            univ.OctetString()),
        namedtype.NamedType('costParameter',
            univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(1, MAX))),
        namedtype.NamedType('blockSize',
            univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(1, MAX))),
        namedtype.NamedType('parallelizationParameter',
            univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(1, MAX))),
        namedtype.OptionalNamedType('keyLength',
            univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(1, MAX)))
    )


# Update the Algorithm Identifier Map and the S/MIME Capability Map

_algorithmIdentifierMapUpdate = {
    id_scrypt: Scrypt_params(),
}

algorithmIdentifierMap.update(_algorithmIdentifierMapUpdate)
