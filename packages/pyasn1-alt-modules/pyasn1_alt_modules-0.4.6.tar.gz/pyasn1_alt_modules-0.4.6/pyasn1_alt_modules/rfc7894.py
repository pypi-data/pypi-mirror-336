#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley.
# Modified by Russ Housley to include the opentypemap manager.
#
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# Alternative Challenge Password Attributes for EST
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc7894.txt
#

from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import univ

from pyasn1_alt_modules import rfc5652
from pyasn1_alt_modules import rfc6402
from pyasn1_alt_modules import rfc7191
from pyasn1_alt_modules import opentypemap


# Since CMS Attributes and CMC Controls both use 'attrType', one map is used

cmsAttributesMap = opentypemap.get('cmsAttributesMap')

cmcControlAttributesMap = cmsAttributesMap


# SingleAttribute is the same as Attribute in RFC 5652, except that the
# attrValues SET must have one and only one member

Attribute = rfc7191.SingleAttribute


# DirectoryString is the same as RFC 5280, except the length is limited to 255

class DirectoryString(univ.Choice):
    pass

DirectoryString.componentType = namedtype.NamedTypes(
    namedtype.NamedType('teletexString', char.TeletexString().subtype(
        subtypeSpec=constraint.ValueSizeConstraint(1, 255))),
    namedtype.NamedType('printableString', char.PrintableString().subtype(
        subtypeSpec=constraint.ValueSizeConstraint(1, 255))),
    namedtype.NamedType('universalString', char.UniversalString().subtype(
        subtypeSpec=constraint.ValueSizeConstraint(1, 255))),
    namedtype.NamedType('utf8String', char.UTF8String().subtype(
        subtypeSpec=constraint.ValueSizeConstraint(1, 255))),
    namedtype.NamedType('bmpString', char.BMPString().subtype(
        subtypeSpec=constraint.ValueSizeConstraint(1, 255)))
)


# OTP Challenge Attribute

id_aa_otpChallenge = univ.ObjectIdentifier('1.2.840.113549.1.9.16.2.56')

ub_aa_otpChallenge = univ.Integer(255)

otpChallenge = Attribute()
otpChallenge['attrType'] = id_aa_otpChallenge
otpChallenge['attrValues'][0] = DirectoryString()


# Revocation Challenge Attribute

id_aa_revocationChallenge = univ.ObjectIdentifier('1.2.840.113549.1.9.16.2.57')

ub_aa_revocationChallenge = univ.Integer(255)

revocationChallenge = Attribute()
revocationChallenge['attrType'] = id_aa_revocationChallenge
revocationChallenge['attrValues'][0] = DirectoryString()


#  EST Identity Linking Attribute

id_aa_estIdentityLinking = univ.ObjectIdentifier('1.2.840.113549.1.9.16.2.58')

ub_aa_est_identity_linking = univ.Integer(255)

estIdentityLinking = Attribute()
estIdentityLinking['attrType'] = id_aa_estIdentityLinking
estIdentityLinking['attrValues'][0] = DirectoryString()


# Update the CMC Control Attributes Map (a.k.a. CMS Attributes Map)

_cmcControlAttributesMapUpdate = {
    id_aa_otpChallenge: DirectoryString(),
    id_aa_revocationChallenge: DirectoryString(),
    id_aa_estIdentityLinking: DirectoryString(),
}

cmcControlAttributesMap.update(_cmcControlAttributesMapUpdate)
