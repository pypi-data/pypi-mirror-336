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
from pyasn1_alt_modules import rfc5280
from pyasn1_alt_modules import rfc3779
from pyasn1_alt_modules import opentypemap


class CertificateExtnTestCase(unittest.TestCase):
    pem_text = """\
MIIECjCCAvKgAwIBAgICAMkwDQYJKoZIhvcNAQELBQAwFjEUMBIGA1UEAxMLcmlw
ZS1uY2MtdGEwIBcNMTcxMTI4MTQzOTU1WhgPMjExNzExMjgxNDM5NTVaMBYxFDAS
BgNVBAMTC3JpcGUtbmNjLXRhMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKC
AQEA0URYSGqUz2myBsOzeW1jQ6NsxNvlLMyhWknvnl8NiBCs/T/S2XuNKQNZ+wBZ
xIgPPV2pFBFeQAvoH/WK83HwA26V2siwm/MY2nKZ+Olw+wlpzlZ1p3Ipj2eNcKrm
it8BwBC8xImzuCGaV0jkRB0GZ0hoH6Ml03umLprRsn6v0xOP0+l6Qc1ZHMFVFb38
5IQ7FQQTcVIxrdeMsoyJq9eMkE6DoclHhF/NlSllXubASQ9KUWqJ0+Ot3QCXr4LX
ECMfkpkVR2TZT+v5v658bHVs6ZxRD1b6Uk1uQKAyHUbn/tXvP8lrjAibGzVsXDT2
L0x4Edx+QdixPgOji3gBMyL2VwIDAQABo4IBXjCCAVowHQYDVR0OBBYEFOhVKx/W
0aT35ATG2OVoDR68Fj/DMA8GA1UdEwEB/wQFMAMBAf8wDgYDVR0PAQH/BAQDAgEG
MIGxBggrBgEFBQcBCwSBpDCBoTA8BggrBgEFBQcwCoYwcnN5bmM6Ly9ycGtpLnJp
cGUubmV0L3JlcG9zaXRvcnkvcmlwZS1uY2MtdGEubWZ0MDIGCCsGAQUFBzANhiZo
dHRwczovL3JyZHAucmlwZS5uZXQvbm90aWZpY2F0aW9uLnhtbDAtBggrBgEFBQcw
BYYhcnN5bmM6Ly9ycGtpLnJpcGUubmV0L3JlcG9zaXRvcnkvMBgGA1UdIAEB/wQO
MAwwCgYIKwYBBQUHDgIwJwYIKwYBBQUHAQcBAf8EGDAWMAkEAgABMAMDAQAwCQQC
AAIwAwMBADAhBggrBgEFBQcBCAEB/wQSMBCgDjAMMAoCAQACBQD/////MA0GCSqG
SIb3DQEBCwUAA4IBAQAVgJjrZ3wFppC8Yk8D2xgzwSeWVT2vtYq96CQQsjaKb8nb
eVz3DwcS3a7RIsevrNVGo43k3AGymg1ki+AWJjvHvJ+tSzCbn5+X6Z7AfYTf2g37
xINVDHru0PTQUargSMBAz/MBNpFG8KThtT7WbJrK4+f/lvx0m8QOlYm2a17iXS3A
GQJ6RHcq9ADscqGdumxmMMDjwED26bGaYdmru1hNIpwF//jVM/eRjBFoPHKFlx0k
Ld/yoCQNmx1kW+xANx4uyWxi/DYgSV7Oynq+C60OucW+d8tIhkblh8+YfrmukJds
V+vo2L72yerdbsP9xjqvhZrLKfsLZjYK4SdYYthi
"""

    def setUp(self):
        self.asn1Spec = rfc5280.Certificate()

    def testDerCodec(self):
        substrate = pem.readBase64fromText(self.pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)
        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))

        extn_list = []
        for extn in asn1Object['tbsCertificate']['extensions']:
            extn_list.append(extn['extnID'])

            if extn['extnID'] == rfc3779.id_pe_ipAddrBlocks:
                s = extn['extnValue']
                addr_blocks, rest = der_decoder(s, rfc3779.IPAddrBlocks())
                self.assertFalse(rest)
                self.assertTrue(addr_blocks.prettyPrint())
                self.assertEqual(s, der_encoder(addr_blocks))

            if extn['extnID'] == rfc3779.id_pe_autonomousSysIds:
                s = extn['extnValue']
                as_ids, rest = der_decoder(s, rfc3779.ASIdentifiers())
                self.assertFalse(rest)
                self.assertTrue(as_ids.prettyPrint())
                self.assertEqual(s, der_encoder(as_ids))

        self.assertIn(rfc3779.id_pe_ipAddrBlocks, extn_list)
        self.assertIn(rfc3779.id_pe_autonomousSysIds, extn_list)

    def testExtensionsMap(self):
        substrate = pem.readBase64fromText(self.pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)
        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))

        certificateExtensionsMap = opentypemap.get('certificateExtensionsMap')
        for extn in asn1Object['tbsCertificate']['extensions']:
            if (extn['extnID'] == rfc3779.id_pe_ipAddrBlocks or
                    extn['extnID'] == rfc3779.id_pe_autonomousSysIds):
                extnValue, rest = der_decoder(extn['extnValue'],
                    asn1Spec=certificateExtensionsMap[extn['extnID']])
                self.assertEqual(extn['extnValue'], der_encoder(extnValue))


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
