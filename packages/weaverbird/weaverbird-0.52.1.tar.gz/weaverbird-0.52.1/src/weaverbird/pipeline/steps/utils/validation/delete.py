"""Validation utilities for Delete step."""
from weaverbird.pipeline.steps.delete import DeleteStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_delete_step_columns(step: DeleteStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the delete step exist in the dataset.
    
    Args:
        step: The delete step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    for col in step.columns:
        if col not in available_columns:
            raise MissingColumnError(column=col, step_name="delete", context="columns parameter")
