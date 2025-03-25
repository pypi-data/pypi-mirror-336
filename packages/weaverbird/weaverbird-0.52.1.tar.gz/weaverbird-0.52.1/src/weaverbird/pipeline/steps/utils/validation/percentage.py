"""Validation utilities for Percentage step."""
from weaverbird.pipeline.steps.percentage import PercentageStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_percentage_step_columns(step: PercentageStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the percentage step exist in the dataset.
    
    Args:
        step: The percentage step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.column not in available_columns:
        raise MissingColumnError(column=step.column, step_name="percentage", context="column parameter")
    
    # Check group_by columns if they exist
    if step.group_by:
        for col in step.group_by:
            if col not in available_columns:
                raise MissingColumnError(column=col, step_name="percentage", context="group_by parameter")
