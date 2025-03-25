"""Validation utilities for Join step."""
from weaverbird.pipeline.steps.join import JoinStep, JoinStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_join_step_columns(step: JoinStep | JoinStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the join step exist in the dataset.
    
    For join steps, we can only validate columns in the left dataset as the right dataset
    might not be loaded yet or could be a separate pipeline.
    
    Args:
        step: The join step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    # For each join condition, check that the left column exists in available columns
    for left_column, _ in step.on:
        if left_column not in available_columns:
            raise MissingColumnError(column=left_column, step_name="join", context="on parameter (left column)")
