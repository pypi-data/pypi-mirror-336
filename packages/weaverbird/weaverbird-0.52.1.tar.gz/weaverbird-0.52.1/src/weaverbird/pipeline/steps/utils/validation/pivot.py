"""Validation utilities for Pivot step."""
from weaverbird.pipeline.steps.pivot import PivotStep, PivotStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_pivot_step_columns(step: PivotStep | PivotStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the pivot step exist in the dataset.
    
    Args:
        step: The pivot step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    # Check index columns
    for col in step.index:
        if col not in available_columns:
            raise MissingColumnError(column=col, step_name="pivot", context="index parameter")
    
    # Check column to pivot
    if step.column_to_pivot not in available_columns:
        raise MissingColumnError(column=step.column_to_pivot, step_name="pivot", context="column_to_pivot parameter")
    
    # Check value column
    if step.value_column not in available_columns:
        raise MissingColumnError(column=step.value_column, step_name="pivot", context="value_column parameter")
