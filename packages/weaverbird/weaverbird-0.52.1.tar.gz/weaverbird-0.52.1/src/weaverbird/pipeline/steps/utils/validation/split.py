"""Validation utilities for Split step."""
from weaverbird.pipeline.steps.split import SplitStep, SplitStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_split_step_columns(step: SplitStep | SplitStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the split step exist in the dataset.
    
    Args:
        step: The split step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.column not in available_columns:
        raise MissingColumnError(column=step.column, step_name="split", context="column parameter")
