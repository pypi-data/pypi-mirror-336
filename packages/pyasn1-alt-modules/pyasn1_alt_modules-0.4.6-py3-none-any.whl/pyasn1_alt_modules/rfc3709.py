#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley with assistance from asn1ate v.0.6.0.
# Modified by Russ Housley to add maps for use with opentypes.
# Modified by Russ Housley to include the opentypemap manager.
# Modified by Russ Housley to add WITH COMPONENTS constraints for
#   requirements from the text, but stated in the ASN.1 module.
#
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# Logotypes in X.509 Certificates
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc3709.txt
#

from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import namedval
from pyasn1.type import tag
from pyasn1.type import univ

from pyasn1_alt_modules import rfc5280
from pyasn1_alt_modules import rfc6170
from pyasn1_alt_modules import opentypemap

certificateExtensionsMap = opentypemap.get('certificateExtensionsMap')

MAX = float('inf')


class HashAlgAndValue(univ.Sequence):
    pass

HashAlgAndValue.componentType = namedtype.NamedTypes(
    namedtype.NamedType('hashAlg', rfc5280.AlgorithmIdentifier()),
    namedtype.NamedType('hashValue', univ.OctetString())
)


class LogotypeDetails(univ.Sequence):
    pass

LogotypeDetails.componentType = namedtype.NamedTypes(
    namedtype.NamedType('mediaType', char.IA5String()),
    namedtype.NamedType('logotypeHash', univ.SequenceOf(
        componentType=HashAlgAndValue()).subtype(
            sizeSpec=constraint.ValueSizeConstraint(1, MAX))),
    namedtype.NamedType('logotypeURI', univ.SequenceOf(
        componentType=char.IA5String()).subtype(
            sizeSpec=constraint.ValueSizeConstraint(1, MAX)))
)


class LogotypeAudioInfo(univ.Sequence):
    pass

LogotypeAudioInfo.componentType = namedtype.NamedTypes(
    namedtype.NamedType('fileSize', univ.Integer()),
    namedtype.NamedType('playTime', univ.Integer()),
    namedtype.NamedType('channels', univ.Integer()),
    namedtype.OptionalNamedType('sampleRate', univ.Integer().subtype(
        implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.OptionalNamedType('language', char.IA5String().subtype(
        implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4)))
)


class LogotypeAudio(univ.Sequence):
    pass

LogotypeAudio.componentType = namedtype.NamedTypes(
    namedtype.NamedType('audioDetails', LogotypeDetails()),
    namedtype.OptionalNamedType('audioInfo', LogotypeAudioInfo())
)


class LogotypeImageType(univ.Integer):
    pass

LogotypeImageType.namedValues = namedval.NamedValues(
    ('grayScale', 0),
    ('color', 1)
)


class LogotypeImageResolution(univ.Choice):
    pass

LogotypeImageResolution.componentType = namedtype.NamedTypes(
    namedtype.NamedType('numBits',
        univ.Integer().subtype(implicitTag=tag.Tag(
            tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('tableSize',
        univ.Integer().subtype(implicitTag=tag.Tag(
            tag.tagClassContext, tag.tagFormatSimple, 2)))
)


class LogotypeImageInfo(univ.Sequence):
    pass

LogotypeImageInfo.componentType = namedtype.NamedTypes(
    namedtype.DefaultedNamedType('type', LogotypeImageType().subtype(
        implicitTag=tag.Tag(tag.tagClassContext,
            tag.tagFormatSimple, 0)).subtype(value='color')),
    namedtype.NamedType('fileSize', univ.Integer()),
    namedtype.NamedType('xSize', univ.Integer()),
    namedtype.NamedType('ySize', univ.Integer()),
    namedtype.OptionalNamedType('resolution', LogotypeImageResolution()),
    namedtype.OptionalNamedType('language', char.IA5String().subtype(
        implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4)))
)


class LogotypeImage(univ.Sequence):
    pass

LogotypeImage.componentType = namedtype.NamedTypes(
    namedtype.NamedType('imageDetails', LogotypeDetails()),
    namedtype.OptionalNamedType('imageInfo', LogotypeImageInfo())
)


class LogotypeData(univ.Sequence):
    pass

LogotypeData.componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('image', univ.SequenceOf(
        componentType=LogotypeImage())),
    namedtype.OptionalNamedType('audio', univ.SequenceOf(
        componentType=LogotypeAudio()).subtype(
            implicitTag=tag.Tag(tag.tagClassContext,
            tag.tagFormatSimple, 1)))
)

LogotypeData.subtypeSpec = constraint.ConstraintsUnion(
    constraint.WithComponentsConstraint(
        ('image', constraint.ComponentPresentConstraint())),
    constraint.WithComponentsConstraint(
        ('audio', constraint.ComponentPresentConstraint()))
)


class LogotypeReference(univ.Sequence):
    pass

LogotypeReference.componentType = namedtype.NamedTypes(
    namedtype.NamedType('refStructHash', univ.SequenceOf(
        componentType=HashAlgAndValue()).subtype(
            sizeSpec=constraint.ValueSizeConstraint(1, MAX))),
    namedtype.NamedType('refStructURI', univ.SequenceOf(
        componentType=char.IA5String()).subtype(
            sizeSpec=constraint.ValueSizeConstraint(1, MAX)))
)


class LogotypeInfo(univ.Choice):
    pass

LogotypeInfo.componentType = namedtype.NamedTypes(
    namedtype.NamedType('direct',
        LogotypeData().subtype(implicitTag=tag.Tag(tag.tagClassContext,
            tag.tagFormatConstructed, 0))),
    namedtype.NamedType('indirect', LogotypeReference().subtype(
        implicitTag=tag.Tag(tag.tagClassContext,
             tag.tagFormatConstructed, 1)))
)

# Other logotype type and associated object identifiers

id_logo_background = univ.ObjectIdentifier('1.3.6.1.5.5.7.20.2')

id_logo_loyalty = univ.ObjectIdentifier('1.3.6.1.5.5.7.20.1')

id_logo_certImage = rfc6170.id_logo_certImage


class OtherLogotypeInfo(univ.Sequence):
    pass

OtherLogotypeInfo.componentType = namedtype.NamedTypes(
    namedtype.NamedType('logotypeType', univ.ObjectIdentifier()),
    namedtype.NamedType('info', LogotypeInfo())
)


# Logotype Certificate Extension

id_pe_logotype = univ.ObjectIdentifier('1.3.6.1.5.5.7.1.12')


class LogotypeExtn(univ.Sequence):
    pass

LogotypeExtn.componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('communityLogos', univ.SequenceOf(
        componentType=LogotypeInfo()).subtype(
            explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.OptionalNamedType('issuerLogo', LogotypeInfo().subtype(
        explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.OptionalNamedType('subjectLogo', LogotypeInfo().subtype(
        explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))),
    namedtype.OptionalNamedType('otherLogos', univ.SequenceOf(
        componentType=OtherLogotypeInfo()).subtype(explicitTag=tag.Tag(
            tag.tagClassContext, tag.tagFormatSimple, 3)))
)

LogotypeExtn.subtypeSpec = constraint.ConstraintsUnion(
    constraint.WithComponentsConstraint(
        ('communityLogos', constraint.ComponentPresentConstraint())),
    constraint.WithComponentsConstraint(
        ('issuerLogo', constraint.ComponentPresentConstraint())),
    constraint.WithComponentsConstraint(
        ('subjectLogo', constraint.ComponentPresentConstraint())),
    constraint.WithComponentsConstraint(
        ('otherLogos', constraint.ComponentPresentConstraint()))
)


# Update the Certificate Extensions Map

_certificateExtensionsMapUpdate = {
    id_pe_logotype: LogotypeExtn(),
}

certificateExtensionsMap.update(_certificateExtensionsMapUpdate)
