"""Validation utilities for Duplicate step."""
from weaverbird.pipeline.steps.duplicate import DuplicateStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_duplicate_step_columns(step: DuplicateStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the duplicate step exist in the dataset.
    
    Args:
        step: The duplicate step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.column not in available_columns:
        raise MissingColumnError(column=step.column, step_name="duplicate", context="column parameter")
