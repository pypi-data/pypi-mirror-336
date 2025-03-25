from io import StringIO

from lxml import etree as ET

from gamslib.validate import utils
from gamslib.validate.abstractvalidator import AbstractValidator
from gamslib.validate.validationresult import ValidationResult


class DTDValidator(AbstractValidator):
    "A XML validator with a DTD."

    def validate(self):
        """Validate well-formedness of an XML file."""
        
        # if no explicit DTD is given, assume ther is one referenced in the xml file
        if self.schema_location is not None:
            result = self._validate_against_explicit_dtd()
        else:
            result = ValidationResult(validated=True, validator=self.__class__.__name__, schema="inline DTD")
            parser = ET.XMLParser(dtd_validation=True)
            try:
                tree = ET.parse(self.file_path, parser)
                result.valid = True
            except ET.XMLSyntaxError as exp:
                result.valid = False
                result.add_error(exp.msg)
        return result

    def _validate_against_explicit_dtd(self):
        """Validate agains a DTD set in the constructor."""

        result = ValidationResult(validated=True, validator=self.__class__.__name__, schema=self.schema_location)

        # load the schema
        schema_data = utils.load_schema(self.schema_location)
        f = StringIO(schema_data.decode("utf-8"))
        dtd = ET.DTD(f)

        # validate the file
        tree = ET.parse(self.file_path)
        is_valid = dtd.validate(tree.getroot())
        errors = dtd.error_log.filter_from_errors() if not is_valid else []
        result.valid = is_valid
        result.errors = errors
        return result
