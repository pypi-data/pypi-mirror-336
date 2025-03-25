import pytest
from gamslib.validate.validationresult import ValidationResult, MultiValidationResult, ValidationError


# ---- tests for ValidationResult ----

def test__init_without_params():
    "Test the __init__ method."
    result = ValidationResult()
    assert result.validator == ""
    assert result.schema == ""
    assert result.errors == []
    with pytest.raises(ValidationError, match="Unvalidated"):
        assert result.valid == False
    
def test__init_with_params():
    "Test the __init__ method with parameters."
    result = ValidationResult(validator="TestValidator", schema="TestSchema")
    assert result.validator == "TestValidator"
    assert result.schema == "TestSchema"
    assert result.errors == []
    with pytest.raises(ValidationError, match="Unvalidated"):
        assert result.valid == False    

def test_valid():
    "Test the valid setter and getter."
    result = ValidationResult()
    with pytest.raises(ValidationError, match="Unvalidated"):
        assert result.valid == False
    result.valid = True
    assert result.valid == True
    result.valid = False
    assert result.valid == False       


def test_add_error():
    "Test the add_error method."
    result = ValidationResult()
    result.add_error("Error 1")
    assert result.errors == ["Error 1"]
    result.add_error("Error 2")
    assert result.errors == ["Error 1", "Error 2"]     


# ---- Tests for MultiValidationResult ----

def test_mv__init_without_params():
    "Test the __init__ method."
    result = MultiValidationResult()
    assert result.validator == ""
    assert result.schema == ""
    assert result.errors == []
    with pytest.raises(ValidationError, match="Unvalidated"):
        assert result.valid == False    

def test_mv__init_with_params():
    "Test the __init__ method with parameters."
    result = MultiValidationResult(validator="TestValidator", schema="TestSchema")
    assert result.validator == "TestValidator"
    assert result.schema == "TestSchema"
    assert result.errors == []
    with pytest.raises(ValidationError, match="Unvalidated"):
        assert result.valid == False            


def test_mv_valid():
    "Test the valid setter and getter."
    result = MultiValidationResult()
    with pytest.raises(ValidationError, match="Unvalidated"):
        assert result.valid == False
    result.valid = True
    assert result.valid == True
    result.valid = False
    assert result.valid == False    

    # when a validation failed, it cannot be made valid again
    result.valid = True
    assert result.valid == False    


def test_mv_add_error():
    "Test the add_error method."
    result = MultiValidationResult()
    result.add_error("Error 1")
    assert result.errors == ["Error 1"]
    result.add_error("Error 2")
    assert result.errors == ["Error 1", "Error 2"]


def test_mv_set_validator():
    "Test the validator getter and setter property."
    result = MultiValidationResult()
    result.validator = ("Validator 1")
    assert result.validator == "Validator 1"
    result.validator = "Validator 2"
    assert result.validator == "Validator 1, Validator 2"


def test_mv_set_schema():
    "Test the schema getter and setter property."
    result = MultiValidationResult()
    result.schema = ("Schema 1")
    assert result.schema == "Schema 1"
    result.schema = "Schema 2"
    assert result.schema == "Schema 1, Schema 2"    

    