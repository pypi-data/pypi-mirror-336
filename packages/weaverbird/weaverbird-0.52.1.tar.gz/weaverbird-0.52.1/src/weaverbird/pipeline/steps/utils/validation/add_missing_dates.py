"""Validation utilities for AddMissingDates step."""
from weaverbird.pipeline.steps.addmissingdates import AddMissingDatesStep, AddMissingDatesStepWithVariables
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_add_missing_dates_step_columns(step: AddMissingDatesStep | AddMissingDatesStepWithVariables, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the add missing dates step exist in the dataset.
    
    Args:
        step: The add missing dates step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.dates_column not in available_columns:
        raise MissingColumnError(column=step.dates_column, step_name="addmissingdates", context="dates_column parameter")
    
    # Check group columns if they exist
    if step.groups:
        for col in step.groups:
            if col not in available_columns:
                raise MissingColumnError(column=col, step_name="addmissingdates", context="groups parameter")
