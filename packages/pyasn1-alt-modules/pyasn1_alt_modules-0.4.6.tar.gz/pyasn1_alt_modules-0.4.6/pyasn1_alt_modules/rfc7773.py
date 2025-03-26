#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley with some assistance from asn1ate v.0.6.0.
# Modified by Russ Housley to include the opentypemap manager.
#
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# Authentication Context Certificate Extension
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc7773.txt
#

from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import univ

from pyasn1_alt_modules import opentypemap

certificateExtensionsMap = opentypemap.get('certificateExtensionsMap')

MAX = float('inf')


# Authentication Context Extension

e_legnamnden = univ.ObjectIdentifier('1.2.752.201')

id_eleg_ce = e_legnamnden + (5, )

id_ce_authContext = id_eleg_ce + (1, )


class AuthenticationContext(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('contextType', char.UTF8String()),
        namedtype.OptionalNamedType('contextInfo', char.UTF8String())
    )

class AuthenticationContexts(univ.SequenceOf):
    componentType = AuthenticationContext()
    subtypeSpec=constraint.ValueSizeConstraint(1, MAX)


# Update the Certificate Extensions Map

_certificateExtensionsMapUpdate = {
    id_ce_authContext: AuthenticationContexts(),
}

certificateExtensionsMap.update(_certificateExtensionsMapUpdate)
