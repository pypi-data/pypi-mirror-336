"""Validation utilities for CumSum step."""
from weaverbird.pipeline.steps.cumsum import CumSumStep, CumSumStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_cumsum_step_columns(step: CumSumStep | CumSumStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the cumsum step exist in the dataset.
    
    Args:
        step: The cumsum step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    # Check columns to sum
    for col, _ in step.to_cumsum:
        if col not in available_columns:
            raise MissingColumnError(column=col, step_name="cumsum", context="to_cumsum parameter")
    
    # Check reference column if it exists
    if step.reference_column and step.reference_column not in available_columns:
        raise MissingColumnError(column=step.reference_column, step_name="cumsum", context="reference_column parameter")
    
    # Check groupby columns if they exist
    if step.groupby:
        for col in step.groupby:
            if col not in available_columns:
                raise MissingColumnError(column=col, step_name="cumsum", context="groupby parameter")
