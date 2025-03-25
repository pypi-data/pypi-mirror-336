from abc import ABC
from dataclasses import dataclass, field
from enum import StrEnum


class SchemaType(StrEnum):
    """Types of validation schemas."""

    DTD_INLINE = "Inline DTD"
    DTD_REFERENCED = "Referenced DTD"
    XSD = "XSD"
    RELAXNG = "RELAX NG"
    SCHEMATRON = "Schematron"


class ValidationError(Exception):
    pass


class ValidationResult:
    """Result of a validation.

    This class is used to store the result of a validation process. It contains information about the
    validator that was used, the schema that was used, and a list of errors that were found during the
    validation process.

    It provides a property `valid` that returns True if the file is valid, and False if not.
    Get access to the list of errors with the `errors` property.
    `validator` and `schema` properties contain the name of the validator and the schema that were used.
    """

    def __init__(self, validator: str = "", schema: str = ""):
        self.validator: str = validator
        self.schema: str = schema
        self.errors: list[str] = []
        self._valid: bool | None = None

    @property
    def valid(self) -> bool:
        if self._valid is None:
            raise ValidationError("Unvalidated.")
        return self._valid

    @valid.setter
    def valid(self, value: bool):
        self._valid = value

    def add_error(self, error_msg: str):
        """Add an error message to the list of errors."""
        self.errors.append(error_msg)

    def __str__(self):
        return (
            f"Validator: {self.validator}, Schema: {self.schema}, Errors: {self.errors}"
        )


class MultiValidationResult(ValidationResult):
    """
    Keep track of the results of multiple validations.

    This class behaves like a normal ValidationResult, but keeps data from multiple validations.
    Some XML Documents for example validate agains RelaxNG and Schematron. This class can be used
    to keep track of the results of both validations.
    """

    def __init__(self, validator: str="", schema: str=""):
        self._valid: bool | None = None
        self._validators: list[str] = []
        self._schemas: list[str] = []
        self.errors = []
        if validator:
            self._validators.append(validator)
        if schema:
            self._schemas.append(schema)

    @property
    def valid(self) -> bool:
        if self._valid is None:
            raise ValidationError("Unvalidated.")
        return self._valid

    @valid.setter
    def valid(self, value: bool):
        # When valid is False, it never can become True again
        if self._valid is None or self._valid is True:
            self._valid = value

    def add_error(self, error_msg: str):
        """Add an error message to the list of errors."""
        self.errors.append(error_msg)

    @property
    def validator(self) -> str:
        return ", ".join(self._validators)

    @validator.setter
    def validator(self, value: str):
        self._validators.append(value)

    @property
    def schema(self) -> str:
        return ", ".join(self._schemas)

    @schema.setter
    def schema(self, value: str):
        self._schemas.append(value)
