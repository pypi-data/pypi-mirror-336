"""Validation utilities for IfThenElse step."""
from weaverbird.pipeline.steps.ifthenelse import IfthenelseStep, IfThenElseStepWithVariables
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError
from weaverbird.pipeline.steps.utils.validation.filter import _validate_condition_columns


def validate_ifthenelse_step_columns(step: IfthenelseStep | IfThenElseStepWithVariables, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the ifthenelse step exist in the dataset.
    
    Args:
        step: The ifthenelse step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    # Conditions in ifthenelse have the same structure as in filter steps
    _validate_condition_columns(step.condition, available_columns, "ifthenelse")
