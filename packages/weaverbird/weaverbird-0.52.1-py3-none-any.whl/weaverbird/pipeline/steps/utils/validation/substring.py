"""Validation utilities for Substring step."""
from weaverbird.pipeline.steps.substring import SubstringStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_substring_step_columns(step: SubstringStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the substring step exist in the dataset.
    
    Args:
        step: The substring step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.column not in available_columns:
        raise MissingColumnError(column=step.column, step_name="substring", context="column parameter")
