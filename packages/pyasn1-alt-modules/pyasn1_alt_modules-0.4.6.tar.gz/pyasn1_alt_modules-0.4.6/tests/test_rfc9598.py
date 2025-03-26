#
# This file is part of pyasn1-alt-modules software.
#
# Copyright (c) 2024-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
import sys
import unittest

from pyasn1.codec.der.decoder import decode as der_decoder
from pyasn1.codec.der.encoder import encode as der_encoder

from pyasn1_alt_modules import pem
from pyasn1_alt_modules import rfc5280
from pyasn1_alt_modules import rfc9598
from pyasn1_alt_modules import opentypemap


class EAITestCase(unittest.TestCase):
    pem_text = "oCAGCCsGAQUFBwgJoBQMEuiAgeW4q0BleGFtcGxlLmNvbQ=="

    def setUp(self):
        self.asn1Spec = rfc5280.GeneralName()

    def testDerCodec(self):
        otherNamesMap = opentypemap.get('otherNamesMap')

        substrate = pem.readBase64fromText(self.pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)
        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))

        self.assertIn(asn1Object['otherName']['type-id'], otherNamesMap)
        self.assertEqual(rfc9598.id_on_SmtpUTF8Mailbox,
                         asn1Object['otherName']['type-id'])

        eai, rest = der_decoder(asn1Object['otherName']['value'],
            asn1Spec=otherNamesMap[asn1Object['otherName']['type-id']])
        self.assertFalse(rest)
        self.assertTrue(eai.prettyPrint())
        self.assertEqual(asn1Object['otherName']['value'], der_encoder(eai))

        self.assertEqual(u'\u8001', eai[0])
        self.assertEqual(u'\u5E2B', eai[1])

    def testOpenTypes(self):
        substrate = pem.readBase64fromText(self.pem_text)
        asn1Object, rest = der_decoder(substrate,
            asn1Spec=self.asn1Spec, decodeOpenTypes=True)
        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))

        self.assertEqual(rfc9598.id_on_SmtpUTF8Mailbox,
                         asn1Object['otherName']['type-id'])
        self.assertEqual(u'\u8001', asn1Object['otherName']['value'][0])
        self.assertEqual(u'\u5E2B', asn1Object['otherName']['value'][1])


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
