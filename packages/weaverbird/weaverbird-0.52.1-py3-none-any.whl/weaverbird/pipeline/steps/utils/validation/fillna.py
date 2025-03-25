"""Validation utilities for Fillna step."""
from weaverbird.pipeline.steps.fillna import FillnaStep, FillnaStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_fillna_step_columns(step: FillnaStep | FillnaStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the fillna step exist in the dataset.
    
    Args:
        step: The fillna step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.column not in available_columns:
        raise MissingColumnError(column=step.column, step_name="fillna", context="column parameter")
