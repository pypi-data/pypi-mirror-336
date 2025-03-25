"""Validation utilities for AbsoluteValue step."""
from weaverbird.pipeline.steps.absolutevalue import AbsoluteValueStep, AbsoluteValueStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_absolute_value_step_columns(step: AbsoluteValueStep | AbsoluteValueStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the absolute value step exist in the dataset.
    
    Args:
        step: The absolute value step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.column not in available_columns:
        raise MissingColumnError(column=step.column, step_name="absolutevalue", context="column parameter")
