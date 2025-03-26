#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley with assistance from asn1ate v.0.6.0.
# Modified by Russ Housley to include the opentypemap manager.
#
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# Attribute Certificate Policies Extension
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc4476.txt
#

from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import univ

from pyasn1_alt_modules import rfc5280
from pyasn1_alt_modules import opentypemap

certificateExtensionsMap = opentypemap.get('certificateExtensionsMap')

policyQualifierInfosMap = opentypemap.get('policyQualifierInfosMap')

MAX = float('inf')


# Imports from RFC 5280

PolicyQualifierId = rfc5280.PolicyQualifierId

PolicyQualifierInfo = rfc5280.PolicyQualifierInfo

UserNotice = rfc5280.UserNotice

id_pkix = rfc5280.id_pkix


# Object Identifiers

id_pe = id_pkix + (1,)

id_pe_acPolicies = id_pe + (15,)

id_qt = id_pkix + (2,)

id_qt_acps = id_qt + (4,)

id_qt_acunotice = id_qt + (5,)


# Attribute Certificate Policies Extension

class ACUserNotice(UserNotice):
    pass


class ACPSuri(char.IA5String):
    pass


class AcPolicyId(univ.ObjectIdentifier):
    pass


class PolicyInformation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('policyIdentifier', AcPolicyId()),
        namedtype.OptionalNamedType('policyQualifiers',
            univ.SequenceOf(componentType=PolicyQualifierInfo()).subtype(
                subtypeSpec=constraint.ValueSizeConstraint(1, MAX)))
    )


class AcPoliciesSyntax(univ.SequenceOf):
    componentType = PolicyInformation()
    subtypeSpec = constraint.ValueSizeConstraint(1, MAX)


# Update the policy qualifier map

_policyQualifierInfosMapUpdate = {
    id_qt_acps: ACPSuri(),
    id_qt_acunotice: UserNotice(),
}

policyQualifierInfosMap.update(_policyQualifierInfosMapUpdate)


# Update the certificate extension map

_certificateExtensionsMapUpdate = {
    id_pe_acPolicies: AcPoliciesSyntax(),
}

certificateExtensionsMap.update(_certificateExtensionsMapUpdate)
