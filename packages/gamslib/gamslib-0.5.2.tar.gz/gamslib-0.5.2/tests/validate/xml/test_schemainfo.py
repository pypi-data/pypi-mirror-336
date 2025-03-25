

import pytest
from gamslib.validate.xml.schemainfo import SchemaInfo, XMLSchemaType

def test_schema_exists(shared_datadir):
    "Test if a schema file exists."
    schema_file = (shared_datadir / "schemas" / "simple.xsd").as_posix()
    assert SchemaInfo.schema_exists(schema_file)
    schema_file = (shared_datadir / "schemas" / "does_not_exist.xsd").as_posix()
    assert not SchemaInfo.schema_exists(schema_file)

    schema_url = "http://gams.uni-graz.at/lido/1.0/lido.xsd"
    assert SchemaInfo.schema_exists(schema_url) 
    schema_url = "https://example.com/foo/bar.xsd"
    assert not SchemaInfo.schema_exists(schema_url)

## Test schema type detection if only the schema location is known
## This will mostly use the last resort: detect by extension
def test_schema_only_dtd(shared_datadir):
    "Test if an external dtd is detected, if only the path to the schema file is given."
    schema_file = (shared_datadir / "schemas" / "simple.dtd").as_posix()
    schemainfo = SchemaInfo(schema_file)
    assert schemainfo.schema_type == XMLSchemaType.DTD
    assert schemainfo.schema_location == schema_file
    assert schemainfo.charset == "utf-8"

def test_schema_only_relaxng(shared_datadir):
    "Test if an external RelaxNG schema is detected, if only the path to the schema file is given."
    schema_file = (shared_datadir / "schemas" / "simple.rng").as_posix()
    schemainfo = SchemaInfo(schema_file)
    assert schemainfo.schema_type == XMLSchemaType.RNG
    assert schemainfo.schema_location == schema_file
    assert schemainfo.charset == "utf-8"

def test_relaxng_compact(shared_datadir):
    "Test if an external RelaxNG Compact schema is detected, if only the path to the schema file is given."
    schema_file = (shared_datadir / "schemas" / "simple.rnc").as_posix()
    schemainfo = SchemaInfo(schema_file)
    assert schemainfo.schema_type == XMLSchemaType.RNC
    assert schemainfo.schema_location == schema_file
    assert schemainfo.charset == "utf-8"

def test_schema_only_schematron(shared_datadir):
    "Test if an external Schematron schema is detected, if only the path to the schema file is given."
    schema_file = (shared_datadir / "schemas" / "simple.sch").as_posix()
    schemainfo = SchemaInfo(schema_file)
    assert schemainfo.schema_type == XMLSchemaType.SCH
    assert schemainfo.schema_location == schema_file
    assert schemainfo.charset == "utf-8"

def test_schema_only_xsd(shared_datadir):
    "Test if an external XSD schema is detected, if only the path to the schema file is given."
    schema_file = (shared_datadir / "schemas" / "simple.xsd").as_posix()
    schemainfo = SchemaInfo(schema_file)
    assert schemainfo.schema_type == XMLSchemaType.XSD
    assert schemainfo.schema_location == schema_file
    assert schemainfo.charset == "utf-8"        


def test_schema_only_unknown(shared_datadir):
    "Test if an unknown schema type is detected, if only the path to the schema file is given."
    schema_file = (shared_datadir / "schemas" / "simple.unknown").as_posix()
    with pytest.raises(ValueError, match="Unknown") as excinfo:
        schemainfo = SchemaInfo(schema_file)

def test_schema_only_schema_not_found(shared_datadir):
    "Test if an error is raised if the schema file does not exist."
    schema_file = (shared_datadir / "schemas" / "not_found.xsd").as_posix()
    with pytest.raises(ValueError, match="not found") as excinfo:
        schemainfo = SchemaInfo(schema_file)


def tests_with_schematypens(shared_datadir, tmp_path):
    "Test if the schema type is detected by the schematypens attribute."
    # as the schema file is ignored when a schemtypens is given, we can use a dummy file
    schema_file = (shared_datadir / "schemas" / "simple.xsd").as_posix()
    schemainfo = SchemaInfo(schema_file, schematypens="http://www.w3.org/2001/XMLSchema")
    assert schemainfo.schema_type == XMLSchemaType.XSD
    assert schemainfo.schema_location == schema_file
    assert schemainfo.charset == "utf-8"

    schemainfo = SchemaInfo(schema_file, schematypens="http://relaxng.org/ns/structure/1.0")
    assert schemainfo.schema_type == XMLSchemaType.RNG
    assert schemainfo.schema_location == schema_file
    assert schemainfo.charset == "utf-8"

    schemainfo = SchemaInfo(schema_file, schematypens="purl.oclc.org/dsdl/schematron")
    assert schemainfo.schema_type == XMLSchemaType.SCH
    assert schemainfo.schema_location == schema_file
    assert schemainfo.charset == "utf-8"

def test_with_mimetype(shared_datadir):
    "Test if the schema type is detected by the mimetype."
    # as the schema file is ignored when a mimetype is given, we can use a dummy file
    schema_file = (shared_datadir / "schemas" / "simple.dtd").as_posix()
    schemainfo = SchemaInfo(schema_file, mimetype="application/xml-dtd")
    assert schemainfo.schema_type == XMLSchemaType.DTD
    assert schemainfo.schema_location == schema_file
    assert schemainfo.charset == "utf-8"

    schema_file = (shared_datadir / "schemas" / "simple.rnc").as_posix()
    schemainfo = SchemaInfo(schema_file, mimetype="application/relax-ng-compact-syntax")
    assert schemainfo.schema_type == XMLSchemaType.RNC
    assert schemainfo.schema_location == schema_file
    assert schemainfo.charset == "utf-8"