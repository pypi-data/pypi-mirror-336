"""Validation utilities for Replace step."""
from weaverbird.pipeline.steps.replace import ReplaceStep, ReplaceStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_replace_step_columns(step: ReplaceStep | ReplaceStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the replace step exist in the dataset.
    
    Args:
        step: The replace step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.search_column not in available_columns:
        raise MissingColumnError(column=step.search_column, step_name="replace", context="search_column parameter")
