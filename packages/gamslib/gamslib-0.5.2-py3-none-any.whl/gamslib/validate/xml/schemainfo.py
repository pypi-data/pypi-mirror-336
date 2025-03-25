"""Provides two classes: XMLSchmeType and SchemaInfo.

XMLSchemaType is an enumeration of the different types of XML schema.

SchemaInfo is a class that represents generic data about a detected schema.
In its most simple usage, it takes a schema location and tries to detect the schema type based on the given data.
But it works more reliable if additional data like mimetype, schematypens, and charset are provided
(which, for some schemas can easily detected from the XML file -- check the xmlvalidator module for examples).
The SchemaInfo class provides a `get_lxml_validator` method that returns an lxml validator object for
the schema.
"""

import enum
from pathlib import Path

from lxml import etree as ET
from lxml import isoschematron

from gamslib.validate import utils


class XMLSchemaType(enum.StrEnum):
    """Enumeration of the different types of XML schema."""

    XSD = "XML Schema Definition"
    RNG = "Relax NG"
    RNC = "Relax NG Compact"
    SCH = "Schematron"
    DTD = "Document Type Definition"


class SchemaInfo:
    """Represent generic data about a detected schema.

    Takes at least the location of the schema file and tries to detect the schema type based on the given data.
    Better results can be achieved if additional data like mimetype, schematypens, and charset are provided.
    """

    def __init__(
        self,
        schema_location: str,
        mimetype="",
        schematypens: str = "",
        charset: str = "utf-8",
    ):
        """Create a SchemaInfo object.

        Tries to detect the schema type based on the given data.
        """
        self.schema_type: XMLSchemaType = None
        if isinstance(schema_location, Path):  # just in case we get a Path object
            schema_location = schema_location.as_posix()
        if not self.schema_exists(schema_location):
            raise ValueError(f"Schema file not found: {schema_location}")
        self.schema_location = schema_location
        self.charset = charset

        # Try various ways to detect the schema type until we have one
        self._detect_by_schematypens(schematypens)
        if self.schema_type is None:
            self._detect_by_mimetype(mimetype)
        if self.schema_type is None:
            self._detect_by_extension(schema_location)
        if self.schema_type is None:
            raise ValueError(
                f"Unknown schema type or schema type not supported: {schema_location}"
            )

    @classmethod
    def schema_exists(cls, schema_location: str) -> bool:
        """Check if the schema file exists."""
        try:
            utils.load_schema(schema_location)
            found = True
        except ValueError:
            found = False
        return found

    def get_lxml_validator(self):
        """Return an lxml validator object for the schema."""
        schema_bytes = utils.load_schema(self.schema_location)
        #doc = ET.parse(schema_bytes.decode(self.charset))
        doc = ET.fromstring(schema_bytes)
        
        if self.schema_type == XMLSchemaType.XSD:
            return ET.XMLSchema(doc)
        elif self.schema_type == XMLSchemaType.RNG:
            return ET.RelaxNG(doc)
        elif self.schema_type == XMLSchemaType.RNC:
            # see https://github.com/djc/rnc2rng/issues/43#issuecomment-1776970457
            return ET.RelaxNG(doc)
        elif self.schema_type == XMLSchemaType.SCH:
            return isoschematron.Schematron(doc)
        elif self.schema_type == XMLSchemaType.DTD:
            return ET.DTD(doc)
        else:
            raise ValueError(f"Unknown schema type: {self.schema_type}")

    def _detect_by_schematypens(self, schematypens) -> None:
        """Detect the schema type by the schematypens attribute."""
        if schematypens == "http://relaxng.org/ns/structure/1.0":
            self.schema_type = XMLSchemaType.RNG
        elif schematypens == "http://www.w3.org/2001/XMLSchema":
            self.schema_type = XMLSchemaType.XSD
        elif schematypens == "purl.oclc.org/dsdl/schematron":
            self.schema_type = XMLSchemaType.SCH

    def _detect_by_mimetype(self, mimetype) -> bool:
        """Detect the schema type by the mimetype.

        This only checks for schema-specific types, not for generic XML types.
        """
        found_type = False
        if mimetype == "application/xml-dtd":
            self.schema_type = XMLSchemaType.DTD
            found_type = True
        elif mimetype == "application/relax-ng-compact-syntax":
            self.schema_type = XMLSchemaType.RNC
            found_type = True
        return found_type

    def _detect_by_extension(self, referenced_schema) -> bool:
        """Detect the schema type by the file extension."""
        found_type = False
        if referenced_schema.endswith(".xsd"):
            self.schema_type = XMLSchemaType.XSD
            found_type = True
        elif referenced_schema.endswith(".rng"):
            self.schema_type = XMLSchemaType.RNG
            found_type = True
        elif referenced_schema.endswith(".rnc"):
            self.schema_type = XMLSchemaType.RNC
            found_type = True
        elif referenced_schema.endswith(".sch"):
            self.schema_type = XMLSchemaType.SCH
            found_type = True
        elif referenced_schema.endswith(".dtd"):
            self.schema_type = XMLSchemaType.DTD
            found_type = True
        return found_type
