from io import StringIO
from gamslib.validate import utils
from gamslib.validate.validationresult import ValidationResult
from ..abstractvalidator import AbstractValidator
from lxml import etree as ET


class GenericXMLValidator(AbstractValidator):
    "A XML validator with unknown and unspecified schema."
    def validate(self):
        """Validate well-formedness of an XML file.
        """
        result = ValidationResult(validated=True, validator=self.__class__.__name__, schema="")

        parser = ET.XMLParser()
        try:
            tree = ET.parse(self.file_path, parser)
            result.valid = True
        except ET.XMLSyntaxError as exp:
            result.valid = False
            result.add_error(exp.msg)
        return result
        
