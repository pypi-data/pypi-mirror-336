"""Validation utilities for Totals step."""
from weaverbird.pipeline.steps.totals import TotalsStep, TotalsStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_totals_step_columns(step: TotalsStep | TotalsStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the totals step exist in the dataset.
    
    Args:
        step: The totals step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    for col in step.aggregate_columns:
        if col not in available_columns:
            raise MissingColumnError(column=col, step_name="totals", context="aggregate_columns parameter")
    
    # Check groups columns if they exist
    if step.groups:
        for col in step.groups:
            if col not in available_columns:
                raise MissingColumnError(column=col, step_name="totals", context="groups parameter")
