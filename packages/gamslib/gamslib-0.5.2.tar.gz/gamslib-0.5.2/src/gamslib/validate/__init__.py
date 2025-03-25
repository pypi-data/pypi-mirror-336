"""Package for validation of data streams and files.
"""



from pathlib import Path

from .xml.xmlvalidator import XMLValidator
from .. import formatdetect
from ..formatdetect.formatinfo import FormatInfo
from ..formatdetect.formatinfo import SubType

from .abstractvalidator import AbstractValidator
from .pdfvalidator import PDFValidator
#from .xml import GenericXMLValidator, TEIValidator, LidoValidator
from .validationresult import ValidationResult

# Maps SubType values to validator classes.
# SUBTYPE_VALIDATOR_MAP = {
#     SubType.TEI: TEIValidator,
#     SubType.LIDO: LidoValidator,
# }

# Maps mimetypes to validator classes.
MIMETYPE_VALIDATOR_MAP = {
    "application/xml": XMLValidator, # fallback for all xml formation with unknown subtype
    "text/xml": XMLValidator, # fallback for all xml formation with unknown subtype
    "application/tei+xml": XMLValidator, # fallback for all xml formation with unknown subtype
    "application/pdf": PDFValidator,
}

SCHEMA_DRIVEN_MIMETYPES = [
    "application/xml",
    "application/tei+xml",
    "text/xml",
    # TODO: Add more schema-driven mimetypes here like "application/json"
]

def make_validator(file_path: Path, format_info: FormatInfo, schema_location: str|None=None) -> AbstractValidator:
    """Return a validator class based on the FormatInfo data.
    
    :param format_info: The format information to use for resolving the validator.
    :param schema_location: The schema location to validate against. If not given, we try to detect the schema from the file if appropriate.
    :return: A validator class.
    :raises ValueError: If no validator is found for the given format.
    """
    #if format_info.subtype in SUBTYPE_VALIDATOR_MAP:
    #    validator_class = SUBTYPE_VALIDATOR_MAP[format_info.subtype]
    if format_info.mimetype in MIMETYPE_VALIDATOR_MAP:
        validator_class = MIMETYPE_VALIDATOR_MAP[format_info.mimetype]
    else:
        raise ValueError(f"No validator class found for {format_info.mimetype}.")
    
    if format_info.mimetype in SCHEMA_DRIVEN_MIMETYPES:
        return validator_class(file_path, schema_location=schema_location, subtype=format_info.subtype)
    else:
        return validator_class(file_path, schema_location=schema_location)


def validate(file_path: Path, schema_location:str|None=None, format_info: FormatInfo|None=None) -> ValidationResult:
    """Validate a file.

    :param file_path: Path to the file to validate.
    :param schema_location: The schema location to validate against. 
           If not given, we try to detect the schema from the file.
    :param format_info: The format information of the file. As detecting the format
              can be expensive, you can pass the format information here if you habe it already.
    :return: A ValidationResult
    """
    if format_info is None:
        format_info = formatdetect.detect_format(file_path)
    # formatdetect was unable to detect the format
    if format_info is None:  
        raise ValueError(f"Could not detect format of {file_path}.")
    validator = make_validator(format_info, schema_location)
    return validator.validate()
    
