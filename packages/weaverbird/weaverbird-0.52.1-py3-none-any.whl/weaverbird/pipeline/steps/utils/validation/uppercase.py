"""Validation utilities for Uppercase step."""
from weaverbird.pipeline.steps.uppercase import UppercaseStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_uppercase_step_columns(step: UppercaseStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the uppercase step exist in the dataset.
    
    Args:
        step: The uppercase step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.column not in available_columns:
        raise MissingColumnError(column=step.column, step_name="uppercase", context="column parameter")
