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
from pyasn1_alt_modules import rfc4055
from pyasn1_alt_modules import rfc5280
from pyasn1_alt_modules import rfc8649
from pyasn1_alt_modules import opentypemap


class RootCertificateExtnTestCase(unittest.TestCase):
    extn_pem_text = """\
MGEGCisGAQQBg5IbAgEEUzBRMA0GCWCGSAFlAwQCAwUABEBxId+rK+WVDLOda2Yk
FFRbqQAztXhs91j/RxHjYJIv/3gleQg3Qix/yQy2rIg3xysjCvHWw8AuYOGVh/sL
GANG
"""

    def setUp(self):
        self.asn1Spec = rfc5280.Extension()

    def testDerCodec(self):
        substrate = pem.readBase64fromText(self.extn_pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)
        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))
        self.assertEqual(rfc8649.id_ce_hashOfRootKey, asn1Object['extnID'])

        hashed_root_key, rest = der_decoder(asn1Object['extnValue'],
            asn1Spec=rfc8649.HashedRootKey())
        self.assertFalse(rest)
        self.assertTrue(hashed_root_key.prettyPrint())
        self.assertEqual(asn1Object['extnValue'], der_encoder(hashed_root_key))
        self.assertEqual(
            rfc4055.id_sha512, hashed_root_key['hashAlg']['algorithm'])

    def testExtensionsMap(self):
        certificateExtensionsMap = opentypemap.get('certificateExtensionsMap')
        substrate = pem.readBase64fromText(self.extn_pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)
        self.assertFalse(rest)
        self.assertEqual(rfc8649.id_ce_hashOfRootKey, asn1Object['extnID'])
        self.assertIn(asn1Object['extnID'], certificateExtensionsMap)


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
