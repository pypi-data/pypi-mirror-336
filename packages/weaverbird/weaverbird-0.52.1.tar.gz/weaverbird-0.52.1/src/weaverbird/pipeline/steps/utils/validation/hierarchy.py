"""Validation utilities for Hierarchy step."""
from weaverbird.pipeline.steps.hierarchy import HierarchyStep
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_hierarchy_step_columns(step: HierarchyStep, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the hierarchy step exist in the dataset.
    
    Args:
        step: The hierarchy step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.hierarchy_column not in available_columns:
        raise MissingColumnError(column=step.hierarchy_column, step_name="hierarchy", context="hierarchy_column parameter")
    
    if step.parent_id_column not in available_columns:
        raise MissingColumnError(column=step.parent_id_column, step_name="hierarchy", context="parent_id_column parameter")
