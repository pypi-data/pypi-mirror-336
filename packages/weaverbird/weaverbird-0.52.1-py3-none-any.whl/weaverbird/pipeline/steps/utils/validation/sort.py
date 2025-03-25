"""Validation utilities for Sort step."""
from weaverbird.pipeline.steps.sort import SortStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_sort_step_columns(step: SortStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the sort step exist in the dataset.
    
    Args:
        step: The sort step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    # Columns is a list of columns or tuples (column, order)
    for col_spec in step.columns:
        if isinstance(col_spec, tuple):
            col = col_spec[0]
        else:
            col = col_spec
            
        if col not in available_columns:
            raise MissingColumnError(column=col, step_name="sort", context="columns parameter")
