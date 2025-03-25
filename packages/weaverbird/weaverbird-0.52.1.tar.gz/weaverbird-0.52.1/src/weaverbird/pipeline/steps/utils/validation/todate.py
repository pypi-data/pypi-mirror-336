"""Validation utilities for ToDate step."""
from weaverbird.pipeline.steps.todate import ToDateStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_todate_step_columns(step: ToDateStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the todate step exist in the dataset.
    
    Args:
        step: The todate step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.column not in available_columns:
        raise MissingColumnError(column=step.column, step_name="todate", context="column parameter")
