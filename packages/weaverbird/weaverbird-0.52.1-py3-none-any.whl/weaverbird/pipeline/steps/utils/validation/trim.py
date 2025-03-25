"""Validation utilities for Trim step."""
from weaverbird.pipeline.steps.trim import TrimStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_trim_step_columns(step: TrimStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the trim step exist in the dataset.
    
    Args:
        step: The trim step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    for col in step.columns:
        if col not in available_columns:
            raise MissingColumnError(column=col, step_name="trim", context="columns parameter")
