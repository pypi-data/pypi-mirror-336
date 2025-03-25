"""Validation utilities for FromDate step."""
from weaverbird.pipeline.steps.fromdate import FromdateStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_fromdate_step_columns(step: FromdateStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the fromdate step exist in the dataset.
    
    Args:
        step: The fromdate step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.column not in available_columns:
        raise MissingColumnError(column=step.column, step_name="fromdate", context="column parameter")
