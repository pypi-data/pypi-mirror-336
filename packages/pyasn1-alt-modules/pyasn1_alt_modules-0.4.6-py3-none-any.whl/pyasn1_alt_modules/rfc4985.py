#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley.
# Modified by Russ Housley to include the opentypemap manager.
#
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# Expression of Service Names in X.509 Certificates
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc4985.txt
#

from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import univ

from pyasn1_alt_modules import rfc5280
from pyasn1_alt_modules import opentypemap

otherNamesMap = opentypemap.get('otherNamesMap')

MAX = float('inf')


# As specified in Appendix A.2 of RFC 4985

id_pkix = rfc5280.id_pkix

id_on = id_pkix + (8, )

id_on_dnsSRV = id_on + (7, )


class SRVName(char.IA5String):
    subtypeSpec = constraint.ValueSizeConstraint(1, MAX)


srvName = rfc5280.AnotherName()
srvName['type-id'] = id_on_dnsSRV
srvName['value'] = SRVName()


# Update the Other Names Map

_otherNamesMapUpdate = {
    id_on_dnsSRV: SRVName(),
}

otherNamesMap.update(_otherNamesMapUpdate)
