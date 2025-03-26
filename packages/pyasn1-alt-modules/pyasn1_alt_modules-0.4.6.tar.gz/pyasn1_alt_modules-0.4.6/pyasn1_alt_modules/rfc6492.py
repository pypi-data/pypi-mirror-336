#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley.
# Modified by Russ Housley to include the opentypemap manager.
#
# Copyright (c) 2021-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# A Protocol for Provisioning Resource Certificates
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc6492.txt
#

from pyasn1.type import univ

from pyasn1_alt_modules import opentypemap

cmsContentTypesMap = opentypemap.get('cmsContentTypesMap')


# Content Type for Provisioning Resource Certificates

id_smime = univ.ObjectIdentifier('1.2.840.113549.1.9.16')

id_ct = id_smime + (1,)

id_ct_xml = id_ct + (28,)

class RPKIXMLProtocolObject(univ.OctetString):
    pass


# Update the CMS Content Types Map

_cmsContentTypesMapUpdate = {
    id_ct_xml: RPKIXMLProtocolObject(),
}

cmsContentTypesMap.update(_cmsContentTypesMapUpdate)
