"""Validation utilities for Concatenate step."""
from weaverbird.pipeline.steps.concatenate import ConcatenateStep, ConcatenateStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_concatenate_step_columns(step: ConcatenateStep | ConcatenateStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the concatenate step exist in the dataset.
    
    Args:
        step: The concatenate step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    for col in step.columns:
        if col not in available_columns:
            raise MissingColumnError(column=col, step_name="concatenate", context="columns parameter")
