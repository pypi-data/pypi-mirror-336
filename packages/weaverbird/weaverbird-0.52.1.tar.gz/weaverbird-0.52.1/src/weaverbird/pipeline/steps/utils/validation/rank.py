"""Validation utilities for Rank step."""
from weaverbird.pipeline.steps.rank import RankStep, RankStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_rank_step_columns(step: RankStep | RankStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the rank step exist in the dataset.
    
    Args:
        step: The rank step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.value_col not in available_columns:
        raise MissingColumnError(column=step.value_col, step_name="rank", context="value_col parameter")
    
    # Check group_by columns if they exist
    if step.group_by:
        for col in step.group_by:
            if col not in available_columns:
                raise MissingColumnError(column=col, step_name="rank", context="group_by parameter")
