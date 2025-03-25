"""Validation utilities for Argmax step."""
from weaverbird.pipeline.steps.argmax import ArgmaxStep, ArgmaxStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_argmax_step_columns(step: ArgmaxStep | ArgmaxStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the argmax step exist in the dataset.
    
    Args:
        step: The argmax step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.column not in available_columns:
        raise MissingColumnError(column=step.column, step_name="argmax", context="column parameter")
    
    # Check group columns if they exist
    if step.groups:
        for col in step.groups:
            if col not in available_columns:
                raise MissingColumnError(column=col, step_name="argmax", context="groups parameter")
