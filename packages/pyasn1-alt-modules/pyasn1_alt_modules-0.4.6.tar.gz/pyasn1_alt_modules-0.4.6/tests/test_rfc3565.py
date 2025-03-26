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
from pyasn1_alt_modules import rfc3565


class AESKeyWrapTestCase(unittest.TestCase):
    kw_alg_id_pem_text = "MAsGCWCGSAFlAwQBLQ=="

    def setUp(self):
        self.asn1Spec = rfc3565.AlgorithmIdentifier()

    def testDerCodec(self):
        substrate = pem.readBase64fromText(self.kw_alg_id_pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)
        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(rfc3565.id_aes256_wrap, asn1Object[0])
        self.assertEqual(substrate, der_encoder(asn1Object))


class AESCBCTestCase(unittest.TestCase):
    aes_alg_id_pem_text = "MB0GCWCGSAFlAwQBKgQQEImWuoUOPwM5mTu1h4oONw=="

    def setUp(self):
        self.asn1Spec = rfc3565.AlgorithmIdentifier()

    def testDerCodec(self):
        substrate = pem.readBase64fromText(self.aes_alg_id_pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)

        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(rfc3565.id_aes256_CBC, asn1Object[0])
        self.assertTrue(asn1Object[1].isValue)
        self.assertEqual(substrate, der_encoder(asn1Object))

    def testOpenTypes(self):
        substrate = pem.readBase64fromText(self.aes_alg_id_pem_text)
        asn1Object, rest = der_decoder(substrate,
            asn1Spec=self.asn1Spec, decodeOpenTypes=True)

        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(rfc3565.id_aes256_CBC, asn1Object[0])

        aes_iv = univ.OctetString(hexValue='108996ba850e3f0339993bb5878a0e37')

        self.assertEqual(aes_iv, asn1Object[1])
        self.assertEqual(substrate, der_encoder(asn1Object))


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
