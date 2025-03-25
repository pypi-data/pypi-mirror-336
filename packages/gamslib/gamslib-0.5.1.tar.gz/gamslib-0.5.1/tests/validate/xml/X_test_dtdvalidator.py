from gamslib.validate.xml.dtdvalidator import DTDValidator


def test_validate_ok(shared_datadir):
    "Test a well-formed XML fitting to a DTD."
    xml_file = shared_datadir / "simple_with_dtd.xml"
    validator = DTDValidator(xml_file)
    result = validator.validate()
    assert result.valid
    assert result.validated
    assert not result.errors
    assert result.validator == "DTDValidator"
    assert result.schema == "inline DTD"

def test_validate_external_dtd_ok(shared_datadir):
    "Test a well-formed XML fitting to a DTD."
    xml_file = shared_datadir / "simple_with_dtd.xml"
    schema_file = (shared_datadir / "simple2.dtd").as_posix()
    validator = DTDValidator(xml_file, schema_location=schema_file)
    result = validator.validate()
    assert result.valid
    assert result.validated
    assert not result.errors
    assert result.validator == "DTDValidator"
    assert result.schema == schema_file

def test_validate_not_ok(shared_datadir):
    "Test a well-formed XML which does not fit to a DTD."
    xml_file = shared_datadir / "simple_with_invalid_dtd.xml"
    validator = DTDValidator(xml_file)
    result = validator.validate()
    assert not result.valid
    assert result.validated
    assert len(result.errors) == 1
    assert "No declaration for element foo" in result.errors[0]
    assert result.validator == "DTDValidator"
    assert result.schema == "inline DTD"


def test_validate_external_dtd_not_found(shared_datadir):
    "With an explicit dtd, which does not exist."
    xml_file = shared_datadir / "simple_with_dtd.xml"
    schema_file = (shared_datadir / "simple2.dtd").as_posix()
    validator = DTDValidator(xml_file, schema_location=schema_file)
    result = validator.validate()
    assert result.valid
    assert result.validated
    assert not result.errors
    assert result.validator == "DTDValidator"
    assert result.schema == schema_file    