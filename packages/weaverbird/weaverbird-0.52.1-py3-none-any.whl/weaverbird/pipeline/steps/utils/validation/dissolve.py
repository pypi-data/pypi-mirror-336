"""Validation utilities for Dissolve step."""
from weaverbird.pipeline.steps.dissolve import DissolveStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_dissolve_step_columns(step: DissolveStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the dissolve step exist in the dataset.
    
    Args:
        step: The dissolve step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    for col in step.on:
        if col not in available_columns:
            raise MissingColumnError(column=col, step_name="dissolve", context="on parameter")
    
    # Check aggregations columns if they exist
    if step.aggregations:
        for agg in step.aggregations:
            for col in agg.columns:
                if col not in available_columns:
                    raise MissingColumnError(column=col, step_name="dissolve", context="aggregation")
