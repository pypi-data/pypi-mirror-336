# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley.
# Modified by Russ Housley to add maps for use with opentypes.
# Modified by Russ Housley to include the opentypemap manager.
#
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# Use of the Advanced Encryption Standard (AES) Encryption
#   Algorithm in the Cryptographic Message Syntax (CMS)
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc3565.txt


from pyasn1.type import constraint
from pyasn1.type import univ

from pyasn1_alt_modules import rfc5280
from pyasn1_alt_modules import opentypemap

algorithmIdentifierMap = opentypemap.get('algorithmIdentifierMap')


class AlgorithmIdentifier(rfc5280.AlgorithmIdentifier):
    pass


class AES_IV(univ.OctetString):
    subtypeSpec = constraint.ValueSizeConstraint(16, 16)


id_aes128_CBC = univ.ObjectIdentifier('2.16.840.1.101.3.4.1.2')

id_aes192_CBC = univ.ObjectIdentifier('2.16.840.1.101.3.4.1.22')

id_aes256_CBC = univ.ObjectIdentifier('2.16.840.1.101.3.4.1.42')


id_aes128_wrap = univ.ObjectIdentifier('2.16.840.1.101.3.4.1.5')

id_aes192_wrap = univ.ObjectIdentifier('2.16.840.1.101.3.4.1.25')

id_aes256_wrap = univ.ObjectIdentifier('2.16.840.1.101.3.4.1.45')


# Update the Algorithm Identifier map

_algorithmIdentifierMapUpdate = {
    id_aes128_CBC: AES_IV(),
    id_aes192_CBC: AES_IV(),
    id_aes256_CBC: AES_IV(),
    id_aes128_wrap: univ.Null(),
    id_aes192_wrap: univ.Null(),
    id_aes256_wrap: univ.Null(),
}

algorithmIdentifierMap.update(_algorithmIdentifierMapUpdate)
