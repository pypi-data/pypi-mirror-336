
from abc import ABC, abstractmethod

from gamslib.validate.validationresult import ValidationResult


class AbstractValidator(ABC):
    """Abstract class for validators.

    Every validator class must inherit from this class and 
    implement the methods. 
    """
    def __init__(self, file_path, schema_location:str|None=None):
        self.file_path = file_path
        self.schema_location = schema_location


    @abstractmethod
    def validate(self) -> ValidationResult:
        "Run the validation process."




        

