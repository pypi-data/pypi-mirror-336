"""Validation utilities for UniqueGroups step."""
from weaverbird.pipeline.steps.uniquegroups import UniqueGroupsStep, UniqueGroupsStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_uniquegroups_step_columns(step: UniqueGroupsStep | UniqueGroupsStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the unique groups step exist in the dataset.
    
    Args:
        step: The unique groups step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    for col in step.on:
        if col not in available_columns:
            raise MissingColumnError(column=col, step_name="uniquegroups", context="on parameter")
