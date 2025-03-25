"""Validation utilities for CompareText step."""
from weaverbird.pipeline.steps.comparetext import CompareTextStep, CompareTextStepWithVariables
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_compare_text_step_columns(step: CompareTextStep | CompareTextStepWithVariables, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the compare text step exist in the dataset.
    
    Args:
        step: The compare text step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.str_column not in available_columns:
        raise MissingColumnError(column=step.str_column, step_name="comparetext", context="str_column parameter")
    
    if step.ref_column not in available_columns:
        raise MissingColumnError(column=step.ref_column, step_name="comparetext", context="ref_column parameter")
