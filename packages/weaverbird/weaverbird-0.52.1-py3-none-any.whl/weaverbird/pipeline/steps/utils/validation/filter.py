"""Validation utilities for Filter step."""
from weaverbird.pipeline.conditions import ComparisonCondition, DateBoundCondition, InclusionCondition, MatchCondition
from weaverbird.pipeline.steps.filter import FilterStep, FilterStepWithVariables
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def _validate_condition_columns(condition, available_columns: set[str], step_name: str) -> None:
    """Validate that all columns referenced in a condition exist in the dataset."""
    if hasattr(condition, "and_") and condition.and_:
        for subcondition in condition.and_:
            _validate_condition_columns(subcondition, available_columns, step_name)
    elif hasattr(condition, "or_") and condition.or_:
        for subcondition in condition.or_:
            _validate_condition_columns(subcondition, available_columns, step_name)
    elif isinstance(condition, (ComparisonCondition, DateBoundCondition, InclusionCondition, MatchCondition)):
        if hasattr(condition, "column") and condition.column and condition.column not in available_columns:
            raise MissingColumnError(column=condition.column, step_name=step_name, context="condition column")


def validate_filter_step_columns(step: FilterStep | FilterStepWithVariables, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the filter step exist in the dataset.
    
    Args:
        step: The filter step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    _validate_condition_columns(step.condition, available_columns, "filter")
