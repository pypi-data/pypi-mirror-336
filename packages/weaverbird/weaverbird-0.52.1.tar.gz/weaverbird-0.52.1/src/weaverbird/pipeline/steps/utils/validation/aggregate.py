"""Validation utilities for aggregate steps."""
from weaverbird.pipeline.steps.aggregate import AggregateStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_aggregate_step_columns(step: AggregateStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the aggregate step exist in the dataset.
    
    Args:
        step: The aggregate step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    # Check 'on' columns
    for col in step.on:
        if col not in available_columns:
            raise MissingColumnError(column=col, step_name="aggregate", context="'on' parameter")
    
    # Check columns used in aggregations
    for agg in step.aggregations:
        for col in agg.columns:
            if col not in available_columns:
                raise MissingColumnError(column=col, step_name="aggregate", context="aggregation")