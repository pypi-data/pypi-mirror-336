"""Validation utilities for Statistics step."""
from weaverbird.pipeline.steps.statistics import StatisticsStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_statistics_step_columns(step: StatisticsStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the statistics step exist in the dataset.
    
    Args:
        step: The statistics step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.column not in available_columns:
        raise MissingColumnError(column=step.column, step_name="statistics", context="column parameter")
    
    # Check groupby columns if they exist
    if step.groupby:
        for col in step.groupby:
            if col not in available_columns:
                raise MissingColumnError(column=col, step_name="statistics", context="groupby parameter")
