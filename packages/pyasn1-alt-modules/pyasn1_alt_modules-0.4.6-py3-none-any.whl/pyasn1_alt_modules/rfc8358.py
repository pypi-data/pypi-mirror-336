#
# This file is part of pyasn1-alt-modules software.
#
# Created by Russ Housley.
# Modified by Russ Housley to include the opentypemap manager.
#
# Copyright (c) 2019-2025, Vigil Security, LLC
# License: http://vigilsec.com/pyasn1-alt-modules-license.txt
#
# Digital Signatures on Internet-Draft Documents
#
# ASN.1 source from:
# https://www.rfc-editor.org/rfc/rfc8358.txt
#

from pyasn1.type import univ

from pyasn1_alt_modules import opentypemap

cmsContentTypesMap = opentypemap.get('cmsContentTypesMap')


# Object Identifiers for the Content Types

id_ct = univ.ObjectIdentifier('1.2.840.113549.1.9.16.1')

id_ct_asciiTextWithCRLF = id_ct + (27, )

id_ct_epub = id_ct + (39, )

id_ct_htmlWithCRLF = id_ct + (38, )

id_ct_pdf = id_ct + (29, )

id_ct_postscript = id_ct + (30, )

id_ct_utf8TextWithCRLF = id_ct + (37, )

id_ct_xml = id_ct + (28, )


# Update the CMS of Content Types Map

_cmsContentTypesMapUpdate = {
    id_ct_asciiTextWithCRLF: univ.OctetString(),
    id_ct_epub: univ.OctetString(),
    id_ct_htmlWithCRLF: univ.OctetString(),
    id_ct_pdf: univ.OctetString(),
    id_ct_postscript: univ.OctetString(),
    id_ct_utf8TextWithCRLF: univ.OctetString(),
    id_ct_xml: univ.OctetString(),
}

cmsContentTypesMap.update(_cmsContentTypesMapUpdate)
