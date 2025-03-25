"""Validation utilities for Unpivot step."""
from weaverbird.pipeline.steps.unpivot import UnpivotStep, UnpivotStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_unpivot_step_columns(step: UnpivotStep | UnpivotStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the unpivot step exist in the dataset.
    
    Args:
        step: The unpivot step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    # Check keep columns
    for col in step.keep:
        if col not in available_columns:
            raise MissingColumnError(column=col, step_name="unpivot", context="keep parameter")
    
    # Check unpivot columns
    for col in step.unpivot:
        if col not in available_columns:
            raise MissingColumnError(column=col, step_name="unpivot", context="unpivot parameter")
