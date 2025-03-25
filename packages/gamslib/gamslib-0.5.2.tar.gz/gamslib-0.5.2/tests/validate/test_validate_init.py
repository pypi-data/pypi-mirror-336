import pytest
from gamslib.formatdetect.formatinfo import FormatInfo, SubType
from gamslib.validate import make_validator


#from gamslib.validate.xml import GenericXMLValidator, TEIValidator, LidoValidator
from gamslib.validate.pdfvalidator import PDFValidator
from gamslib.validate.xml.xmlvalidator import XMLValidator

@pytest.mark.parametrize("mimetype, subtype, expected_validator", [
    ('application/xml', None, XMLValidator),
    ('application/xml', SubType.TEI, XMLValidator),
    ('application/xml', SubType.LIDO, XMLValidator),
    ('application/tei+xml', SubType.TEI, XMLValidator),
])
def test_resolve_validatorclass_from_mimetype(mimetype, subtype, expected_validator, tmp_path):
    "Test for resolving a validator class from a mimetype."
    formatinfo = FormatInfo('foo',  mimetype=mimetype, subtype=subtype)
    result = make_validator(tmp_path, formatinfo)
    assert isinstance(result, expected_validator)
    assert  result.subtype == subtype


    