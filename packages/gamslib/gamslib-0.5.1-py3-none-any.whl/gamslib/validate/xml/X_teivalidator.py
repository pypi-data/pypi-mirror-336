
from gamslib.formatdetect.formatinfo import FormatInfo
from gamslib.validate.xml.xmlvalidator import XMLValidator


class TEIValidator(XMLValidator):

    DEFAULT_SCHEMA_LOCATION = "https://www.tei-c.org/release/xml/tei/custom/schema/xsd/tei_all.xsd"

    def __init__(self, file_path, schema_location:str|None=None):
        if schema_location is None:
            schema_location = self.DEFAULT_SCHEMA_LOCATION 
            # TODO: Additionally we have to check the TEI source for a schema reference!
        super().__init__(file_path, schema_location, FormatInfo(subtype=SubType.TEI))

    # def validate(self) -> ValidationResult:
    #     """Validate the file.
        
    #     :return: A ValidationResult object.
    #     """
    #     # validate the file
    #     return ValidationResult(True, "TEI validation successful.")