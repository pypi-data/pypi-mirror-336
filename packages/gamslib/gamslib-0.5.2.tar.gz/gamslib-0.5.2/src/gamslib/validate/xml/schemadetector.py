"""Provides functions to detect schema references in XML files.

The main function is detect_schemata, which tries to find all schema references in an XML file.
"""

import enum
from pathlib import Path

import uritools
from lxml import etree as ET

from gamslib.formatdetect.formatinfo import FormatInfo, SubType
from gamslib.validate.xml.schemainfo import SchemaInfo, XMLSchemaType


def join_reference_path(xml_path, schema_reference) -> str:
    """Join a reference path with the path of the XML file.

    If schema_reference looks like a path (relative) to xml_path,
    we resolve it and return the resolved path.
    Otherwise, we return schema_reference as is.
    """
    if schema_reference.startswith("http"):
        return schema_reference
    new_path = (xml_path.parent / schema_reference).resolve()
    return new_path.as_posix() if new_path.is_file() else schema_reference


def find_schemata_in_processing_instructions(
    tree: ET.ElementTree, xml_file: Path
) -> list[SchemaInfo]:
    """Return all schema referenced in an XML processing instruction.

    This primarily indented as a helper function for find_schemata_in_file.
    We need the path of the xml file to resolve relative paths in the PI.
    """
    # collect PI nodes in front and after the root element
    schemata = []
    for node in tree.xpath("preceding-sibling::node()"):
        if hasattr(node, "target") and node.target == "xml-model":
            schemata.append(
                SchemaInfo(
                    join_reference_path(xml_file, node.attrib["href"]),
                    node.attrib.get("type", ""),
                    node.attrib.get("schemtypens", ""),
                    node.attrib.get("charset", "utf-8"),
                )
            )
    for node in tree.xpath("following-sibling::node()"):
        if hasattr(node, "target") and node.target == "xml-model":
            schemata.append(
                SchemaInfo(
                    join_reference_path(xml_file, node.attrib["href"]),
                    node.attrib.get("type", ""),
                    node.attrib.get("schemtypens", ""),
                    node.attrib.get("charset", "utf-8"),
                )
            )
    return schemata


def find_schemata_in_root_element(
    tree: ET.ElementTree, xml_file: Path
) -> list[SchemaInfo]:
    """Return all schema referenced in an XML root element via schemaLoction or noNamespaceSchemaLocation.

    We currently only support usage in the root element, not in subelements.
    Usage of schemaLocation in subelements is handeled directly in xmlvalidator.py.

    This primarily indented as a helper function for find_schemata_in_file.
    We need the path of the xml file to resolve relative paths in the root element.
    """
    namespaces = {"xsi": "http://www.w3.org/2001/XMLSchema-instance"}
    schemata = []
    root_element = tree.getroot()
    schema_location_name = f"{{{namespaces['xsi']}}}schemaLocation"
    no_namespace_schema_location_name = (
        f"{{{namespaces['xsi']}}}noNamespaceSchemaLocation"
    )
    schema_refs = []
    if no_namespace_schema_location_name in root_element.attrib:
        schema_refs += root_element.attrib[no_namespace_schema_location_name].split()
    if schema_location_name in root_element.attrib:
        schema_refs += root_element.attrib[schema_location_name].split()[1::2]
    for schema_ref in schema_refs:
        schemata.append(
            SchemaInfo(
                join_reference_path(xml_file, schema_ref),
                XMLSchemaType.XSD,
                charset=root_element.attrib.get("encoding", "utf-8"),
            )
        )
    return schemata


def find_dtd_in_tree(tree, xml_file: Path) -> list[SchemaInfo]:
    """Create list with 0 or 1 SchemaInfo objects for a referenced DTD file.

    We need the path of the xml file to resolve relative paths in the DTD.
    """
    dtd = tree.docinfo.externalDTD
    if dtd is None:
        dtd = tree.docinfo.internalDTD
    if dtd:
        schema_ref = join_reference_path(xml_file, dtd.system_url)
        return  [SchemaInfo(schema_ref, XMLSchemaType.DTD)]  
    return []



def find_schemata_in_tree(tree: ET.ElementTree, xml_file: Path) -> list[SchemaInfo]:
    """Try to find all schema references in the given XML tree.

    This function tries to find all schema references in the given XML tree.
    It uses the following methods to find the schema references:
    - processing instructions
    - root element attributes
    - DTDs

    It returns a List of SchemaInfo objects containing one SchemaInfo object for each found schema.
    """
    schemata: list[SchemaInfo] = []
    schemata = find_schemata_in_processing_instructions(tree, xml_file)
    schemata += find_schemata_in_root_element(tree, xml_file)
    schemata += find_dtd_in_tree(tree, xml_file)

    # TODO: What about inline DTDs?
    return schemata


def detect_schemata(
    tree: ET.ElementTree, xml_file: Path, formatinfo: FormatInfo
) -> list[SchemaInfo]:
    """Return a list of SchemaInfo objects for the given XML file."""
    schemata = find_schemata_in_tree(tree, xml_file)
    if not schemata:
        # if we did not find any referenced schema in the tree, we use default schema for the subtype
        if formatinfo == SubType.TEI:
            schemata.append(
                SchemaInfo(
                    "http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng",
                    schematypens="http://relaxng.org/ns/structure/1.0",
                )
            )
        elif formatinfo == SubType.LIDO:
            schemata.append(
                SchemaInfo(
                    "http://www.lido-schema.org/schema/v1.0/lido-v1.0.rng",
                    schematypens="http://relaxng.org/ns/structure/1.0",
                )
            )
    return schemata
