#
# This file is part of pyasn1-alt-modules software.
#
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
import sys
import unittest

from pyasn1.codec.der.decoder import decode as der_decoder
from pyasn1.codec.der.encoder import encode as der_encoder

from pyasn1_alt_modules import pem
from pyasn1_alt_modules import rfc5652
from pyasn1_alt_modules import rfc6019
from pyasn1_alt_modules import opentypemap


class BinarySigningTimeTestCase(unittest.TestCase):
    pem_text = "MBUGCyqGSIb3DQEJEAIuMQYCBFy/hlQ="

    def setUp(self):
        self.asn1Spec = rfc5652.Attribute()

    def testDerCodec(self):
        substrate = pem.readBase64fromText(self.pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)

        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))
        self.assertEqual(rfc6019.id_aa_binarySigningTime, asn1Object['attrType'])

        bintime, rest = der_decoder(
            asn1Object['attrValues'][0], asn1Spec=rfc6019.BinaryTime())

        self.assertEqual(0x5cbf8654, bintime)

    def testOpenTypes(self):
        substrate = pem.readBase64fromText(self.pem_text)
        asn1Object, rest = der_decoder(substrate, 
            asn1Spec=self.asn1Spec, decodeOpenTypes=True)
        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))
        self.assertEqual(0x5cbf8654, asn1Object['attrValues'][0])

    def testAttributesMap(self):
        substrate = pem.readBase64fromText(self.pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)

        cmsAttributesMap = opentypemap.get('cmsAttributesMap')
        self.assertIn(asn1Object['attrType'], cmsAttributesMap)


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
