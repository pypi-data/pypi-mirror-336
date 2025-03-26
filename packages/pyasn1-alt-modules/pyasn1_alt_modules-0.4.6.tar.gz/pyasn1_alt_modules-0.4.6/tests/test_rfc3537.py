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
from pyasn1_alt_modules import rfc3537
from pyasn1_alt_modules import rfc5751
from pyasn1_alt_modules import opentypemap


class SMIMECapabilitiesTestCase(unittest.TestCase):
    smime_capabilities_pem_text = "MCIwDwYLKoZIhvcNAQkQAwwFADAPBgsqhkiG9w0BCRADCwUA"

    def setUp(self):
        self.asn1Spec = rfc5751.SMIMECapabilities()

    def testDerCodec(self):
        openTypesMap = opentypemap.get('smimeCapabilityMap')

        substrate = pem.readBase64fromText(self.smime_capabilities_pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)
        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))

        count = 0
        for cap in asn1Object:
            self.assertEqual(der_encoder(univ.Null("")), cap['parameters'])
            self.assertIn(cap['capabilityID'], openTypesMap)
            count += 1

        self.assertEqual(count, 2)

    def testOpenTypes(self):
        openTypesMap = opentypemap.get('smimeCapabilityMap')

        asn1Spec=rfc5751.SMIMECapabilities()
        substrate = pem.readBase64fromText(self.smime_capabilities_pem_text)
        asn1Object, rest = der_decoder(
            substrate, asn1Spec=self.asn1Spec,
            openTypes=openTypesMap, decodeOpenTypes=True)
        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))

        count = 0
        for cap in asn1Object:
            self.assertEqual(univ.Null(""), cap['parameters'])
            self.assertIn(cap['capabilityID'], openTypesMap)
            count += 1

        self.assertEqual(count, 2)


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
