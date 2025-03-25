"""Validation utilities for Simplify step."""
from weaverbird.pipeline.steps.simplify import SimplifyStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_simplify_step_columns(step: SimplifyStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the simplify step exist in the dataset.
    
    Args:
        step: The simplify step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.geometry_column not in available_columns:
        raise MissingColumnError(column=step.geometry_column, step_name="simplify", context="geometry_column parameter")
