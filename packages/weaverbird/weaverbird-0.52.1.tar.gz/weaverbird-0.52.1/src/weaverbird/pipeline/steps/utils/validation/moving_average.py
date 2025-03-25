"""Validation utilities for MovingAverage step."""
from weaverbird.pipeline.steps.moving_average import MovingAverageStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_moving_average_step_columns(step: MovingAverageStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the moving average step exist in the dataset.
    
    Args:
        step: The moving average step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.column_to_average not in available_columns:
        raise MissingColumnError(
            column=step.column_to_average, step_name="moving_average", context="column_to_average parameter"
        )
    
    # Check group_by columns if they exist
    if step.group_by:
        for col in step.group_by:
            if col not in available_columns:
                raise MissingColumnError(column=col, step_name="moving_average", context="group_by parameter")
