"""Validation utilities for Top step."""
from weaverbird.pipeline.steps.top import TopStep, TopStepWithVariables
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_top_step_columns(step: TopStep | TopStepWithVariables, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the top step exist in the dataset.
    
    Args:
        step: The top step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.rank_on not in available_columns:
        raise MissingColumnError(column=step.rank_on, step_name="top", context="rank_on parameter")
    
    # Check groups columns if they exist
    if step.groups:
        for col in step.groups:
            if col not in available_columns:
                raise MissingColumnError(column=col, step_name="top", context="groups parameter")
