"""Validation utilities for DateExtract step."""
from weaverbird.pipeline.steps.date_extract import DateExtractStep, DateExtractStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_date_extract_step_columns(step: DateExtractStep | DateExtractStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the date extract step exist in the dataset.
    
    Args:
        step: The date extract step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.column not in available_columns:
        raise MissingColumnError(column=step.column, step_name="date_extract", context="column parameter")
