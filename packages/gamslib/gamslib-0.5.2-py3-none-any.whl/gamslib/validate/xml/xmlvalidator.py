from gamslib.validate.abstractvalidator import AbstractValidator
from gamslib.validate.validationresult import ValidationResult, MultiValidationResult
from gamslib.validate.xml.schemainfo import SchemaInfo
from ...formatdetect.formatinfo import FormatInfo
from lxml import etree as ET
from . import schemadetector


class XMLValidator(AbstractValidator):
    DEFAULT_SCHEMA_LOCATION = None

    def __init__(
        self,
        file_path,
        schema_location: str | None = None,
        subtype: FormatInfo | None = None,
    ):
        super().__init__(file_path, schema_location)
        self.subtype = subtype

    def validate(self) -> ValidationResult:
        """Validate the file.

        :return: A ValidationResult object.
        """
        try:
            tree = ET.parse(self.file_path, ET.XMLParser())
            schemata = []
            # if we have an explicit schema location, we use this schema (and only this one!)
            if self.schema_location is not None:
                schemata.append(SchemaInfo(self.schema_location))
            # this has to be handled differently because we need more than on validator
            elif self.has_subschemas(tree): 
                return self._validate_subschema_document(tree)
            else:
                schemata = schemadetector.detect_schemata(tree, self.file_path, self.subtype)

            # if we have schemata, we validate against them
            if schemata:
                return self._validate_external_schemata(tree, schemata)
            
            # if we did not find any schema, this can be because there is an internal DTD schema or no schema at all
            if tree.docinfo.doctype:
                return self._validate_internal_dtd_schema()
            else: # no schema and no DTD
                result = ValidationResult(validator="XMLValidator")
                result.valid = True
                return result
        except ET.XMLSyntaxError as exp:  # raised when not well-formed
            validation_result = ValidationResult()
            validation_result.valid = False
            validation_result.validator = "XMLValidator"
            validation_result.add_error(exp.msg)
            return validation_result

    @classmethod
    def has_subschemas(self, tree: ET.ElementTree) -> bool:
        """Check if the XML file uses subschemas.

        The schemaLocation can be used in root element, but also in other elements,
        referencing different schemata. This is eg. common in METS files.
        This method return True, if schemaLocation or noNamespaceSchemaLocation is used
        in an element below the root element.
        """
        namespaces = {"xsi": "http://www.w3.org/2001/XMLSchema-instance"}

        root = tree.getroot()
        for elem in root.iter():
            result = elem.xpath(".//*[@xsi:schemaLocation]", namespaces=namespaces)
            if result:
                return True
            result = elem.xpath(
                ".//*[@xsi:noNamespaceSchemaLocation]", namespaces=namespaces
            )
            if result:
                return True
        return False

    def _validate_subschema_document(self, tree: ET.ElementTree) -> ValidationResult:
        """Validates a document with subschemas.

        This method is used when child elements refere to a schema 
        different from the schema referenced in the root element.
        """
        validation_result = MultiValidationResult()
        XSI = "http://www.w3.org/2001/XMLSchema-instance"
        namespaces = {"xsi": XSI}
        for elem in tree.xpath(
            "//*[@xsi:schemaLocation or @xsi:noNamespaceSchemaLocation]",
            namespaces=namespaces,
        ):
            referenced_schema = elem.attrib.get(f"{{{XSI}}}noNamespaceSchemaLocation")
            if referenced_schema is None:
                referenced_schema = elem.attrib[f"{{{XSI}}}schemaLocation"].split()[1]
            schema_location = schemadetector.join_reference_path(
                self.file_path, referenced_schema
            )
            schema_info = SchemaInfo(schema_location)
            validator = schema_info.get_lxml_validator()
            validation_result.validator = validator.__class__.__name__
            validation_result.schema = schema_location
            try:
                validator.assertValid(elem)
                validation_result.valid = True
            except AssertionError as exp:
                validation_result.valid = False
                validation_result.add_error(exp.msg)
            except ET.DocumentInvalid as exp:  
                validation_result.valid = False
                validation_result.add_error(exp.error_log.last_error)
        return validation_result

    def _validate_internal_dtd_schema(self) -> ValidationResult:
        """Validate the tree against the internal DTD schema."""
        try:
            tree = ET.parse(self.file_path, ET.XMLParser(dtd_validation=True))
            validation_result = ValidationResult("internal DTD", "internal DTD")
            validation_result.valid = True
        except ET.XMLSyntaxError as exp:
            validation_result = ValidationResult()
            validation_result.valid = False
            validation_result.add_error(exp.msg)
            return validation_result

    def _validate_external_schemata(
        self, tree: ET.ElementTree, schemata: list[SchemaInfo]
    ) -> ValidationResult:
        """Validate the tree against all external schemata."""
        # Apply all schemata to the tree
        validation_result = MultiValidationResult()
        for schema in schemata:
            validator = schema.get_validator()
            validation_result = ValidationResult.validator = validator = (
                validator.__class__.__name__
            )
            validation_result.schema = schema.schema_location
            try:
                validator.assertValid(tree)
                validation_result.valid = True
            except AssertionError as exp:
                validation_result.valid = False
                validation_result.add_error(exp.msg)
        return validation_result
