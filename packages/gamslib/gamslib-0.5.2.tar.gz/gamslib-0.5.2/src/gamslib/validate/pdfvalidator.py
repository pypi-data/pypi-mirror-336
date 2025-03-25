from gamslib.validate.validationresult import ValidationResult
from .abstractvalidator import AbstractValidator


class PDFValidator(AbstractValidator):


    def validate(self):
        """Validate a PDF file.
        
        TODO: Does no validation at all at the moment.
        """
        result = ValidationResult(validated=False, validator=self.__class__.__name__, schema="")
        return result
