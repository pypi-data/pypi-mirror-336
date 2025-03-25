"""Validation utilities for ReplaceText step."""
from weaverbird.pipeline.steps.replacetext import ReplaceTextStep, ReplaceTextStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_replacetext_step_columns(step: ReplaceTextStep | ReplaceTextStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the replacetext step exist in the dataset.
    
    Args:
        step: The replacetext step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.search_column not in available_columns:
        raise MissingColumnError(column=step.search_column, step_name="replacetext", context="search_column parameter")
