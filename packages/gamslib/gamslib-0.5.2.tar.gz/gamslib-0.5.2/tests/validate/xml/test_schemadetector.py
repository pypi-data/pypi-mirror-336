import lxml.etree as ET
from gamslib.validate.xml import schemadetector
from gamslib.validate.xml.schemainfo import SchemaInfo, XMLSchemaType


def test_join_reference_same_dir(tmp_path):
    """join_reference resolves a relative schema reference.
    Test if it works if the xml file and schema file are in the same directory.
    """

    xml_file = tmp_path / "simple_with_rng_and_sch.xml"
    schema_reference = "simple.rng"
    schema_path = xml_file.parent / schema_reference
    schema_path.touch()
    new_path = schemadetector.join_reference_path(xml_file, schema_reference)
    assert new_path == (xml_file.parent / schema_reference).as_posix()


def test_join_reference_relative_dir(tmp_path):
    "Test join_reference if xml file and schema are in different subdirectories."
    xml_file = tmp_path / "foo" / "simple_with_rng_and_sch.xml"
    schema_reference = "../bar/simple.rng"
    schema_path = tmp_path / "bar" / "simple.rng"
    schema_path.parent.mkdir(parents=True)
    xml_file.parent.mkdir()
    schema_path.touch()
    new_path = schemadetector.join_reference_path(xml_file, schema_reference)
    assert new_path == schema_path.as_posix()


def test_join_reference_non_existing_schema(tmp_path):
    """Test join_reference if referenced schema does not exist."
    Should return the original reference. (to be handled somewere else).
    """
    xml_file = tmp_path / "minimal_with_sch.xml"
    schema_reference = "missing.rng"
    new_path = schemadetector.join_reference_path(xml_file, schema_reference)
    assert new_path == "missing.rng"


def test_join_reference_absolute_path(tmp_path):
    "Test join_reference if schema is reference by URL."
    xml_file = tmp_path / "simple_with_rng_and_sch.xml"
    schema_reference = "http://example.com/simple.rng"
    new_path = schemadetector.join_reference_path(xml_file, schema_reference)
    assert new_path == schema_reference



## -------------- test the single find_schema_in_xx functions -----------------------------


def test_find_schema_in_processing_instructions(shared_datadir):
    xml_file = shared_datadir / "simple_with_rng_and_sch_in_pi.xml"
    root = ET.parse(xml_file)
    schemata = schemadetector.find_schemata_in_processing_instructions(root, xml_file)
    assert len(schemata) == len(["rng", "sch", "rng2"])

    assert schemata[0].schema_type == XMLSchemaType.SCH
    assert schemata[0].charset == "utf-8"
    assert schemata[0].schema_location == (shared_datadir / "schemas" / "simple.sch").as_posix()

    assert schemata[1].schema_type == XMLSchemaType.RNG
    assert schemata[1].charset == "utf-8"
    assert (
        schemata[1].schema_location
        == (shared_datadir / "schemas" / "simple.rng").as_posix()
    )

    assert schemata[2].schema_type == XMLSchemaType.RNG
    assert schemata[2].charset == "utf-8"
    assert (
        schemata[2].schema_location
        == (shared_datadir / "schemas" / "simple2.rng").as_posix()
    )


def test_find_schema_in_processing_instructions_url(shared_datadir, monkeypatch):
    "Test find_schema_in_processing_instructions with URL referenced schemas."
    xml_file = shared_datadir / "simple_with_rng_and_sch_in_pi.xml"
    # lxml does not allow to change PI attributes. So we have to change the PI attributes in the xml source
    xml = xml_file.read_text()
    xml = xml.replace('href="schemas/simple.sch"', 'href="http://example.com/simple.sch"')
    xml = xml.replace(
        'href="./schemas/simple.rng"', 'href="http://example.com/simple.rng"'
    )
    xml = xml.replace(
        'href="./schemas/simple2.rng"', 'href="http://example.com/simple2.rng"'
    )
    root = ET.fromstring(xml)
    # replace the href attribute of the xml-model PI with an URL
    for node in root.xpath("preceding-sibling::node()"):
        if node.target == "xml-model":
            if ".sch" in node.attrib["href"]:
                node.attrib["href"] = "http://example.com/simple.sch"
            else:
                node.attrib["href"] = "http://example.com/simple.rng"
    for node in root.xpath("following-sibling::node()"):
        if node.target == "xml-model":
            node.attrib["href"] = "http://example.com/simple2.rng"

    # schemadetector calls the schema_exists method of SchemaInfo. We have to mock it.
    monkeypatch.setattr(SchemaInfo, "schema_exists", lambda self, x: True)
    schemata = schemadetector.find_schemata_in_processing_instructions(root, xml_file)
    assert len(schemata) == len(["sch", "rng", "rng2"])
    assert schemata[0].schema_type == XMLSchemaType.SCH
    assert schemata[0].schema_location == "http://example.com/simple.sch"
    assert schemata[1].schema_type == XMLSchemaType.RNG
    assert schemata[1].schema_location == "http://example.com/simple.rng"
    assert schemata[2].schema_type == XMLSchemaType.RNG
    assert schemata[2].schema_location == "http://example.com/simple2.rng"


def test_find_schema_in_root_element(shared_datadir):
    xml_file = shared_datadir / "simple_with_xsd_in_root.xml"
    root = ET.parse(xml_file)
    schemata = schemadetector.find_schemata_in_root_element(root, xml_file)
    assert len(schemata) == 1
    assert schemata[0].schema_type == XMLSchemaType.XSD
    assert schemata[0].charset == "utf-8"
    assert (
        schemata[0].schema_location
        == (shared_datadir / "schemas" / "simple.xsd").as_posix()
    )

def test_find_schmes_external_dtd(shared_datadir):
    xml_file = shared_datadir / "simple_with_external_dtd.xml"
    schema_file = shared_datadir / "schemas" / "simple.dtd"
    root = ET.parse(xml_file)
    schemata = schemadetector.find_dtd_in_tree(root, xml_file)
    assert len(schemata) == 1
    assert schemata[0].schema_location == schema_file.as_posix()
    assert schemata[0].schema_type == XMLSchemaType.DTD
    assert schemata[0].charset == "utf-8"