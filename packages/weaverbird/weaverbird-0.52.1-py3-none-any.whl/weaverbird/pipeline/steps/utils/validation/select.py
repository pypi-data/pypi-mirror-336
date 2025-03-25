"""Validation utilities for Select step."""
from weaverbird.pipeline.steps.select import SelectStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_select_step_columns(step: SelectStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the select step exist in the dataset.
    
    Args:
        step: The select step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    for col in step.columns:
        if col not in available_columns:
            raise MissingColumnError(column=col, step_name="select", context="columns parameter")
