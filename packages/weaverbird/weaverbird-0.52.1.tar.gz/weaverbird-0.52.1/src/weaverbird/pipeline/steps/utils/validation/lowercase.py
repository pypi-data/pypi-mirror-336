"""Validation utilities for Lowercase step."""
from weaverbird.pipeline.steps.lowercase import LowercaseStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_lowercase_step_columns(step: LowercaseStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the lowercase step exist in the dataset.
    
    Args:
        step: The lowercase step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.column not in available_columns:
        raise MissingColumnError(column=step.column, step_name="lowercase", context="column parameter")
