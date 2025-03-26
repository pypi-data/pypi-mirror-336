# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley.
# Modified by Russ Housley to include the opentypemap manager.
#
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# Traceable Anonymous Certificate
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc5480.txt

from pyasn1.type import namedtype
from pyasn1.type import univ
from pyasn1.type import useful

from pyasn1_alt_modules import rfc5652
from pyasn1_alt_modules import opentypemap

cmsContentTypesMap = opentypemap.get('cmsContentTypesMap')


# Imports from RFC 5652

ContentInfo = rfc5652.ContentInfo

EncapsulatedContentInfo = rfc5652.EncapsulatedContentInfo

id_data = rfc5652.id_data


# Object Identifiers

id_KISA = univ.ObjectIdentifier((1, 2, 410, 200004,))


id_npki = id_KISA + (10,)


id_attribute = id_npki + (1,)


id_kisa_tac = id_attribute + (1,)


id_kisa_tac_token = id_kisa_tac + (1,)


id_kisa_tac_tokenandblindbash = id_kisa_tac + (2,)


id_kisa_tac_tokenandpartially = id_kisa_tac + (3,)


# Structures for Traceable Anonymous Certificate (TAC)

class UserKey(univ.OctetString):
    pass


class Timeout(useful.GeneralizedTime):
    pass


class BlinedCertificateHash(univ.OctetString):
    pass


class PartiallySignedCertificateHash(univ.OctetString):
    pass


class Token(ContentInfo):
    pass


class TokenandBlindHash(ContentInfo):
    pass


class TokenandPartiallySignedCertificateHash(ContentInfo):
    pass


# Added to the module in RFC 5636 for the CMS Content Type Map

class TACToken(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('userKey', UserKey()),
        namedtype.NamedType('timeout', Timeout())
    )


class TACTokenandBlindHash(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('token', Token()),
        namedtype.NamedType('blinded', BlinedCertificateHash())
    )


class TACTokenandPartiallySignedCertificateHash(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('token', Token()),
        namedtype.NamedType('partially', PartiallySignedCertificateHash())
    )


# Update the CMS Content Type Map

_cmsContentTypesMapUpdate = {
    id_kisa_tac_token: TACToken(),
    id_kisa_tac_tokenandblindbash: TACTokenandBlindHash(),
    id_kisa_tac_tokenandpartially: TACTokenandPartiallySignedCertificateHash(),
}

cmsContentTypesMap.update(_cmsContentTypesMapUpdate)
