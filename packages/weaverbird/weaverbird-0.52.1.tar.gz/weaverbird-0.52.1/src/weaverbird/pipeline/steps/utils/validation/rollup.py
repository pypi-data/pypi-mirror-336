"""Validation utilities for Rollup step."""
from weaverbird.pipeline.steps.rollup import RollupStep, RollupStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_rollup_step_columns(step: RollupStep | RollupStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the rollup step exist in the dataset.
    
    Args:
        step: The rollup step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    # Check hierarchy columns
    for col in step.hierarchy:
        if col not in available_columns:
            raise MissingColumnError(column=col, step_name="rollup", context="hierarchy parameter")
    
    # Check aggregations if they exist
    if step.aggregations:
        for agg in step.aggregations:
            for col in agg.columns:
                if col not in available_columns:
                    raise MissingColumnError(column=col, step_name="rollup", context="aggregation")
