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
from pyasn1_alt_modules import rfc5990
from pyasn1_alt_modules import opentypemap


class RSAKEMTestCase(unittest.TestCase):
    pem_text = """\
MEcGCyqGSIb3DQEJEAMOMDgwKQYHKIGMcQICBDAeMBkGCiuBBRCGSAksAQIwCwYJ
YIZIAWUDBAIBAgEQMAsGCWCGSAFlAwQBBQ==
"""

    def setUp(self):
        self.asn1Spec = rfc5280.AlgorithmIdentifier()

    def testDerCodec(self):
        substrate = pem.readBase64fromText(self.pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)

        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))
        self.assertEqual(rfc5990.id_rsa_kem, asn1Object['algorithm'])

        algorithmIdentifierMap = opentypemap.get('algorithmIdentifierMap')
        rsa_kem_p, rest = der_decoder(asn1Object['parameters'],
            asn1Spec=algorithmIdentifierMap[rfc5990.id_rsa_kem])

        self.assertFalse(rest)
        self.assertTrue(rsa_kem_p.prettyPrint())
        self.assertEqual(asn1Object['parameters'], der_encoder(rsa_kem_p))
        self.assertEqual(rfc5990.id_kem_rsa, rsa_kem_p['kem']['algorithm'])

        kem_rsa_p, rest = der_decoder(rsa_kem_p['kem']['parameters'],
            asn1Spec=algorithmIdentifierMap[rfc5990.id_kem_rsa])

        self.assertFalse(rest)
        self.assertTrue(kem_rsa_p.prettyPrint())
        self.assertEqual(
            rsa_kem_p['kem']['parameters'], der_encoder(kem_rsa_p))
        self.assertEqual(16, kem_rsa_p['keyLength'])
        self.assertEqual(
            rfc5990.id_kdf_kdf3, kem_rsa_p['keyDerivationFunction']['algorithm'])

        kdf_p, rest = der_decoder(
            kem_rsa_p['keyDerivationFunction']['parameters'],
            asn1Spec=algorithmIdentifierMap[rfc5990.id_kdf_kdf3])

        self.assertFalse(rest)
        self.assertTrue(kdf_p.prettyPrint())
        self.assertEqual(
            kem_rsa_p['keyDerivationFunction']['parameters'],
            der_encoder(kdf_p))

    def testOpenTypes(self):
        substrate = pem.readBase64fromText(self.pem_text)
        asn1Object, rest = der_decoder(
            substrate, asn1Spec=self.asn1Spec, decodeOpenTypes=True)

        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))
        self.assertEqual(rfc5990.id_rsa_kem, asn1Object['algorithm'])
        self.assertEqual(
            rfc5990.id_kem_rsa, asn1Object['parameters']['kem']['algorithm'])
        self.assertEqual(
            16, asn1Object['parameters']['kem']['parameters']['keyLength'])


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
