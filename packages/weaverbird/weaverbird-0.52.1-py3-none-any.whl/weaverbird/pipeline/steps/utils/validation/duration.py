"""Validation utilities for Duration step."""
from weaverbird.pipeline.steps.duration import DurationStep, DurationStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_duration_step_columns(step: DurationStep | DurationStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the duration step exist in the dataset.
    
    Args:
        step: The duration step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.start_date_column not in available_columns:
        raise MissingColumnError(column=step.start_date_column, step_name="duration", context="start_date_column parameter")
    
    if step.end_date_column not in available_columns:
        raise MissingColumnError(column=step.end_date_column, step_name="duration", context="end_date_column parameter")
