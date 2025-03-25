"""Validation utilities for Argmin step."""
from weaverbird.pipeline.steps.argmin import ArgminStep, ArgminStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_argmin_step_columns(step: ArgminStep | ArgminStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the argmin step exist in the dataset.
    
    Args:
        step: The argmin step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.column not in available_columns:
        raise MissingColumnError(column=step.column, step_name="argmin", context="column parameter")
    
    # Check group columns if they exist
    if step.groups:
        for col in step.groups:
            if col not in available_columns:
                raise MissingColumnError(column=col, step_name="argmin", context="groups parameter")
