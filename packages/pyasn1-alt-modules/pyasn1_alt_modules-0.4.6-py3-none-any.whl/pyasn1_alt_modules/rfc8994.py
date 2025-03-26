#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley with some assistance from asn1ate v.0.6.0.
# Modified by Russ Housley to include the opentypemap manager.
#
# Copyright (c) 2021-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# Autonomic Control Plane (ACP) Node Name in X.509 Certificates
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc8994.txt
#

from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import univ

from pyasn1_alt_modules import rfc5280
from pyasn1_alt_modules import opentypemap

otherNamesMap = opentypemap.get('otherNamesMap')

MAX = float('inf')


# Autonomic Control Plane (ACP) Node Name

id_pkix = rfc5280.id_pkix

id_on = id_pkix + (8, )

id_on_AcpNodeName = id_on + (10, )


class AcpNodeName(char.IA5String):
    subtypeSpec = constraint.ValueSizeConstraint(1, MAX)


on_AcpNodeName = rfc5280.AnotherName()
on_AcpNodeName['type-id'] = id_on_AcpNodeName
on_AcpNodeName['value'] = AcpNodeName()


# Update the Other Names Map

_otherNamesMapUpdate = {
    id_on_AcpNodeName: AcpNodeName(),
}

otherNamesMap.update(_otherNamesMapUpdate)
