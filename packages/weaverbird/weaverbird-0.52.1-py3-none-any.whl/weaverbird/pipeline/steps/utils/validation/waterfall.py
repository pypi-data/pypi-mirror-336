"""Validation utilities for Waterfall step."""
from weaverbird.pipeline.steps.waterfall import WaterfallStep, WaterfallStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_waterfall_step_columns(step: WaterfallStep | WaterfallStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the waterfall step exist in the dataset.
    
    Args:
        step: The waterfall step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.value not in available_columns:
        raise MissingColumnError(column=step.value, step_name="waterfall", context="value parameter")
    
    if step.labels and step.labels not in available_columns:
        raise MissingColumnError(column=step.labels, step_name="waterfall", context="labels parameter")
    
    # Check groups if they exist
    if step.groups:
        for col in step.groups:
            if col not in available_columns:
                raise MissingColumnError(column=col, step_name="waterfall", context="groups parameter")
