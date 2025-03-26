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

from pyasn1_alt_modules import pem
from pyasn1_alt_modules import rfc5280
from pyasn1_alt_modules import rfc5913
from pyasn1_alt_modules import rfc5755
from pyasn1_alt_modules import rfc3114
from pyasn1_alt_modules import opentypemap


class ClearanceTestCase(unittest.TestCase):
    cert_pem_text = """\
MIIDhzCCAw6gAwIBAgIJAKWzVCgbsG5GMAoGCCqGSM49BAMDMD8xCzAJBgNVBAYT
AlVTMQswCQYDVQQIDAJWQTEQMA4GA1UEBwwHSGVybmRvbjERMA8GA1UECgwIQm9n
dXMgQ0EwHhcNMTkxMTAyMTg0MjE4WhcNMjAxMTAxMTg0MjE4WjBmMQswCQYDVQQG
EwJVUzELMAkGA1UECBMCVkExEDAOBgNVBAcTB0hlcm5kb24xEDAOBgNVBAoTB0V4
YW1wbGUxDDAKBgNVBAsTA1BDQTEYMBYGA1UEAxMPcGNhLmV4YW1wbGUuY29tMHYw
EAYHKoZIzj0CAQYFK4EEACIDYgAEPf5vbgAqbE5dn6wbiCx4sCCcn1BKSrHmCfiW
C9QLSGVNGHifQwPt9odGXjRiQ7QwpZ2wRD6Z91v+fk85XXLE3kJQCQdPIHFUY5EM
pvS7T6u6xrmwnlVpUURPTOxfc55Oo4IBrTCCAakwHQYDVR0OBBYEFCbqJQ8LMiAo
pNdaCo3/Ldy9f1RlMG8GA1UdIwRoMGaAFPI12zQE2qVV8r1pA5mwYuziFQjBoUOk
QTA/MQswCQYDVQQGEwJVUzELMAkGA1UECAwCVkExEDAOBgNVBAcMB0hlcm5kb24x
ETAPBgNVBAoMCEJvZ3VzIENBggkA6JHWBpFPzvIwDwYDVR0TAQH/BAUwAwEB/zAL
BgNVHQ8EBAMCAYYwQgYJYIZIAYb4QgENBDUWM1RoaXMgY2VydGlmaWNhdGUgY2Fu
bm90IGJlIHRydXN0ZWQgZm9yIGFueSBwdXJwb3NlLjAVBgNVHSAEDjAMMAoGCCsG
AQUFBw0CMAoGA1UdNgQDAgECMIGRBggrBgEFBQcBFQSBhDCBgTBZBgsqhkiG9w0B
CRAHAwMCBeAxRjBEgAsqhkiG9w0BCRAHBIE1MDMMF0xBVyBERVBBUlRNRU5UIFVT
RSBPTkxZDBhIVU1BTiBSRVNPVVJDRVMgVVNFIE9OTFkwEQYLKoZIhvcNAQkQBwID
AgTwMBEGCyqGSIb3DQEJEAcBAwIF4DAKBggqhkjOPQQDAwNnADBkAjAZSD+BVqzc
1l0fDoH3LwixjxvtddBHbJsM5yBek4U9b2yWL2KEmwV02fTgof3AjDECMCTsksmx
5f3i5DSYfe9Q1heJlEJLd1hgZmfvUYNnCU3WrdmYzyoNdNTbg7ZFMoxsXw==
"""

    def setUp(self):
        self.asn1Spec = rfc5280.Certificate()

    def testDerCodec(self):
        substrate = pem.readBase64fromText(self.cert_pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)

        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))

        cat_value_found = False
        certificateExtensionsMap = opentypemap.get('certificateExtensionsMap')
        securityCategoryMap = opentypemap.get('securityCategoryMap')

        for extn in asn1Object['tbsCertificate']['extensions']:
            if extn['extnID'] == rfc5913.id_pe_clearanceConstraints:
                self.assertIn(extn['extnID'], certificateExtensionsMap)
                ev, rest = der_decoder(extn['extnValue'],
                    asn1Spec=certificateExtensionsMap[extn['extnID']])
                self.assertFalse(rest)
                self.assertTrue(ev.prettyPrint())
                self.assertEqual(extn['extnValue'], der_encoder(ev))

                for c in ev:
                    if c['policyId'] == rfc3114.id_tsp_TEST_Whirlpool:
                        for sc in c['securityCategories']:
                            self.assertIn(sc['type'], securityCategoryMap)
                            scv, rest = der_decoder(sc['value'],
                                asn1Spec=securityCategoryMap[sc['type']])
                            self.assertFalse(rest)
                            self.assertTrue(scv.prettyPrint())
                            self.assertEqual(sc['value'], der_encoder(scv))

                            for cat in scv:
                                self.assertIn('USE ONLY', cat)
                                cat_value_found = True

        self.assertTrue(cat_value_found)

    def testOpenTypes(self):
        substrate = pem.readBase64fromText(self.cert_pem_text)
        asn1Object, rest = der_decoder(
            substrate, asn1Spec=self.asn1Spec, decodeOpenTypes=True)
        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))

        cat_value_found = False
        certificateExtensionsMap = opentypemap.get('certificateExtensionsMap')
        securityCategoryMap = opentypemap.get('securityCategoryMap')

        for extn in asn1Object['tbsCertificate']['extensions']:
            if extn['extnID'] == rfc5913.id_pe_clearanceConstraints:
                self.assertIn(extn['extnID'], certificateExtensionsMap)
                ev, rest = der_decoder(extn['extnValue'],
                    asn1Spec=certificateExtensionsMap[extn['extnID']],
                    decodeOpenTypes=True)
                self.assertFalse(rest)
                self.assertTrue(ev.prettyPrint())
                self.assertEqual(extn['extnValue'], der_encoder(ev))

                for c in ev:
                    if c['policyId'] == rfc3114.id_tsp_TEST_Whirlpool:
                        for sc in c['securityCategories']:
                            self.assertIn(sc['type'], securityCategoryMap)
                            for cat in sc['value']:
                                self.assertIn('USE ONLY', cat)
                                cat_value_found = True

        self.assertTrue(cat_value_found)


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
