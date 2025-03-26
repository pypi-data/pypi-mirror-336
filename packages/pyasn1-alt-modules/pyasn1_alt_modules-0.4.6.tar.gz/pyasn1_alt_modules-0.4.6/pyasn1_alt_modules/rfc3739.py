#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley with assistance from asn1ate v.0.6.0.
# Modified by Russ Housley to add WithComponentsConstraints to
#   enforce the requirements that are indicated in comments.
# Modified by Russ Housley to include the opentypemap manager.
# Modified by CBonnell to align the SemanticsInformation
#   definition with https://www.rfc-editor.org/errata/eid7802.
#
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# Qualified Certificates
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc3739.txt
# https://www.rfc-editor.org/errata/eid7802
#

from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import namedval
from pyasn1.type import opentype
from pyasn1.type import univ
from pyasn1.type import useful

from pyasn1_alt_modules import rfc5280
from pyasn1_alt_modules import opentypemap

certificateAttributesMap = opentypemap.get('certificateAttributesMap')

certificateExtensionsMap = opentypemap.get('certificateExtensionsMap')

qcStatementsMap = opentypemap.get('qcStatementsMap')

MAX = float('inf')


# Imports from RFC 5280

AlgorithmIdentifier = rfc5280.AlgorithmIdentifier

AttributeType = rfc5280.AttributeType

DirectoryString = rfc5280.DirectoryString

GeneralName = rfc5280.GeneralName

id_pkix = rfc5280.id_pkix

id_pe = rfc5280.id_pe


# Arc for QC personal data attributes

id_pda = id_pkix + (9, )


# Arc for QC statements

id_qcs = id_pkix + (11, )


# Personal data attributes

id_pda_dateOfBirth = id_pda + (1, )

class DateOfBirth(useful.GeneralizedTime):
    pass


id_pda_placeOfBirth = id_pda + (2, )

class PlaceOfBirth(DirectoryString):
    pass


id_pda_gender = id_pda + (3, )

class Gender(char.PrintableString):
    subtypeSpec = constraint.ConstraintsIntersection(
        constraint.ValueSizeConstraint(1, 1),
        constraint.SingleValueConstraint('M', 'F', 'm', 'f')
    )


id_pda_countryOfCitizenship = id_pda + (4, )

class CountryOfCitizenship(char.PrintableString):
    subtypeSpec = constraint.ValueSizeConstraint(2, 2)
    # ISO 3166 Country Code


id_pda_countryOfResidence = id_pda + (5, )

class CountryOfResidence(char.PrintableString):
    subtypeSpec = constraint.ValueSizeConstraint(2, 2)
    # ISO 3166 Country Code


# Biometric info certificate extension

id_pe_biometricInfo = id_pe + (2, )


class PredefinedBiometricType(univ.Integer):
    namedValues = namedval.NamedValues(
        ('picture', 0),
        ('handwritten-signature', 1)
    )
    subtypeSpec = constraint.SingleValueConstraint(0, 1)


class TypeOfBiometricData(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('predefinedBiometricType', PredefinedBiometricType()),
        namedtype.NamedType('biometricDataOid', univ.ObjectIdentifier())
    )


class BiometricData(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('typeOfBiometricData', TypeOfBiometricData()),
        namedtype.NamedType('hashAlgorithm', AlgorithmIdentifier()),
        namedtype.NamedType('biometricDataHash', univ.OctetString()),
        namedtype.OptionalNamedType('sourceDataUri', char.IA5String())
    )


class BiometricSyntax(univ.SequenceOf):
    componentType = BiometricData()


# QC Statements certificate extension
# NOTE: This extension does not allow to mix critical and
# non-critical Qualified Certificate Statements. Either all
# statements must be critical or all statements must be
# non-critical.

id_pe_qcStatements = id_pe + (3, )


class NameRegistrationAuthorities(univ.SequenceOf):
    componentType = GeneralName()
    subtypeSpec=constraint.ValueSizeConstraint(1, MAX)


class QCStatement(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('statementId', univ.ObjectIdentifier()),
        namedtype.OptionalNamedType('statementInfo', univ.Any(),
            openType=opentype.OpenType('statementId', qcStatementsMap))
    )


class QCStatements(univ.SequenceOf):
    componentType = QCStatement()


class SemanticsInformation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.OptionalNamedType('semanticsIdentifier',
            univ.ObjectIdentifier()),
        namedtype.OptionalNamedType('nameRegistrationAuthorities',
            NameRegistrationAuthorities())
    )
    subtypeSpec = constraint.ConstraintsUnion(
        constraint.WithComponentsConstraint(
            ('semanticsIdentifier', constraint.ComponentPresentConstraint())),
        constraint.WithComponentsConstraint(
            ('nameRegistrationAuthorities', constraint.ComponentPresentConstraint()))
    )


id_qcs = id_pkix + (11, )


id_qcs_pkixQCSyntax_v1 = id_qcs + (1, )


id_qcs_pkixQCSyntax_v2 = id_qcs + (2, )


# Update the Certificate Extensions Map

_certificateExtensionsMapUpdate = {
     id_pe_biometricInfo: BiometricSyntax(),
     id_pe_qcStatements: QCStatements(),
}

certificateExtensionsMap.update(_certificateExtensionsMapUpdate)


# Update the Certificate Attribute Map

_certificateAttributesMapUpdate = {
    id_pda_dateOfBirth: DateOfBirth(),
    id_pda_placeOfBirth: PlaceOfBirth(),
    id_pda_gender: Gender(),
    id_pda_countryOfCitizenship: CountryOfCitizenship(),
    id_pda_countryOfResidence: CountryOfResidence(),
}

certificateAttributesMap.update(_certificateAttributesMapUpdate)
