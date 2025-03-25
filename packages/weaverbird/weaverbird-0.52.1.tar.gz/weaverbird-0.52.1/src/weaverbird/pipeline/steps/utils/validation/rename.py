"""Validation utilities for Rename step."""
from weaverbird.pipeline.steps.rename import RenameStep, RenameStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_rename_step_columns(step: RenameStep | RenameStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the rename step exist in the dataset.
    
    Args:
        step: The rename step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    # Check all old column names to be renamed
    for old_name, _ in step.to_rename:
        if old_name not in available_columns:
            raise MissingColumnError(column=old_name, step_name="rename", context="to_rename parameter (old name)")
