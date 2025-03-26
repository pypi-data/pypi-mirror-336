#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley with assistance from asn1ate v.0.6.0.
# Modified by Russ Housley to include the opentypemap manager.
#
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# Diffie-Hellman Key Agreement
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc3820.txt
#

from pyasn1.type import namedtype
from pyasn1.type import univ

from pyasn1_alt_modules import opentypemap

certificateExtensionsMap = opentypemap.get('certificateExtensionsMap')


class ProxyCertPathLengthConstraint(univ.Integer):
    pass


class ProxyPolicy(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('policyLanguage', univ.ObjectIdentifier()),
        namedtype.OptionalNamedType('policy', univ.OctetString())
    )


class ProxyCertInfoExtension(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.OptionalNamedType('pCPathLenConstraint',
            ProxyCertPathLengthConstraint()),
        namedtype.NamedType('proxyPolicy', ProxyPolicy())
    )


id_pkix = univ.ObjectIdentifier((1, 3, 6, 1, 5, 5, 7, ))


id_pe = id_pkix + (1, )

id_pe_proxyCertInfo = id_pe + (14, )


id_ppl = id_pkix + (21, )

id_ppl_anyLanguage = id_ppl + (0, )

id_ppl_inheritAll = id_ppl + (1, )

id_ppl_independent = id_ppl + (2, )


# Update the Certificate Extensions Map

_certificateExtensionsMapUpdate = {
    id_pe_proxyCertInfo: ProxyCertInfoExtension(),	
}

certificateExtensionsMap.update(_certificateExtensionsMapUpdate)
