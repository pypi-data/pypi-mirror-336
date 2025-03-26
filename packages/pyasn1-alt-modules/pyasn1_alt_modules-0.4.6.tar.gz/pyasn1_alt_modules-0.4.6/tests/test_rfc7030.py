#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
import sys
import unittest

from pyasn1.codec.der.decoder import decode as der_decoder
from pyasn1.codec.der.encoder import encode as der_encoder
from pyasn1.type import univ

from pyasn1_alt_modules import pem
from pyasn1_alt_modules import rfc5652
from pyasn1_alt_modules import rfc7030
from pyasn1_alt_modules import opentypemap


class CSRAttrsTestCase(unittest.TestCase):
    pem_text = """\
MEEGCSqGSIb3DQEJBzASBgcqhkjOPQIBMQcGBSuBBAAiMBYGCSqGSIb3DQEJDjEJ
BgcrBgEBAQEWBggqhkjOPQQDAw==
"""

    the_oids = (
        univ.ObjectIdentifier('1.2.840.113549.1.9.7'),
        univ.ObjectIdentifier('1.2.840.10045.4.3.3')
    )

    the_attrTypes = (
        univ.ObjectIdentifier('1.2.840.10045.2.1'),
        univ.ObjectIdentifier('1.2.840.113549.1.9.14'),
    )

    the_attrVals = (
        '1.3.132.0.34',
        '1.3.6.1.1.1.1.22',
    )

    def setUp(self):
        self.asn1Spec = rfc7030.CsrAttrs()

    def testDerCodec(self):
        substrate = pem.readBase64fromText(self.pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)

        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))

        for attr_or_oid in asn1Object:
            if attr_or_oid.getName() == 'oid':
                self.assertIn(attr_or_oid['oid'], self.the_oids)

            if attr_or_oid.getName() == 'attribute':
                self.assertIn(
                    attr_or_oid['attribute']['attrType'], self.the_attrTypes)

    def testOpenTypes(self):
        openTypesMap = opentypemap.get('cmsAttributesMap').copy()
        for at in self.the_attrTypes:
            openTypesMap.update({at: univ.ObjectIdentifier()})

        substrate = pem.readBase64fromText(self.pem_text)
        asn1Object, rest = der_decoder(substrate,
            asn1Spec=self.asn1Spec, openTypes=openTypesMap, decodeOpenTypes=True)
        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))

        for attr_or_oid in asn1Object:
            if attr_or_oid.getName() == 'attribute':
                valString = attr_or_oid['attribute']['attrValues'][0].prettyPrint()

                if attr_or_oid['attribute']['attrType'] == self.the_attrTypes[0]:
                    self.assertEqual(self.the_attrVals[0], valString)

                if attr_or_oid['attribute']['attrType'] == self.the_attrTypes[1]:
                    self.assertEqual(self.the_attrVals[1], valString)


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
